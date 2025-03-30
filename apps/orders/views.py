from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.authentication.authentication import JWTAuthentication
from apps.authentication.permissions import IsAdminOrCustomer
from bson.objectid import ObjectId
from ecommerce.settings import mongo_db
from django.utils.timezone import now
from celery_tasks.tasks import send_order_confirmation_email

class OrderViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrCustomer]

    orders_collection = mongo_db['orders']
    carts_collection = mongo_db['carts']

    def create(self, request):
        """
        Create a new order for the authenticated user, with optional discount application.
        """
        user_email = request.user.email  # Use dot notation
        cart = self.carts_collection.find_one({"user_email": user_email})
    
        if not cart or not cart.get("cart_items"):
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
    
        # Get the discount code from the request
        discount_code = request.data.get("discount_code")
        discount = None
        discount_amount = 0
    
        if discount_code:
            # Validate the discount code
            discount = mongo_db['discounts'].find_one({"code": discount_code, "user_email": user_email, "active": True})
            if not discount:
                return Response({"error": "Invalid or inactive discount code."}, status=status.HTTP_400_BAD_REQUEST)
    
            # Check if the discount is within the valid date range
            from datetime import datetime
            now = datetime.utcnow()
            valid_from = datetime.fromisoformat(discount["valid_from"])
            valid_to = datetime.fromisoformat(discount["valid_to"])
    
            if not (valid_from <= now <= valid_to):
                return Response({"error": "Discount code is not valid at this time."}, status=status.HTTP_400_BAD_REQUEST)
    
            # Calculate the discount amount
            total_amount = sum(item["quantity"] * item["price"] for item in cart["cart_items"])
            discount_amount = (total_amount * float(discount["percentage"])) / 100
    
        # Create the order
        order_data = {
            "user_email": user_email,
            "items": cart["cart_items"],
            "status": "Pending",
            "created_at": now().isoformat(),
            "discount_code": discount_code if discount else None,
            "discount_amount": discount_amount,
            "total_amount": total_amount - discount_amount if discount else total_amount,
        }
        result = self.orders_collection.insert_one(order_data)
    
        # Clear the cart after placing the order
        self.carts_collection.update_one(
            {"user_email": user_email},
            {"$set": {"cart_items": []}}
        )
    
        order_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
        send_order_confirmation_email.delay(order_data["_id"], user_email)
        return Response(order_data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        Retrieve all orders for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        orders = list(self.orders_collection.find({"user_email": user_email}))

        # Convert ObjectId to string
        for order in orders:
            order["_id"] = str(order["_id"])

        return Response(orders, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific order by ID for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        try:
            order = self.orders_collection.find_one({"_id": ObjectId(pk), "user_email": user_email})
            if not order:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

            order["_id"] = str(order["_id"])  # Convert ObjectId to string
            return Response(order, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid order ID."}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update an order (e.g., status) for the authenticated user.
        """
        if request.user.role != "admin":
            return Response({"detail": "You do not have permission to update the order status."}, status=status.HTTP_403_FORBIDDEN)

        user_email = request.user.email  # Use dot notation
        try:
            order = self.orders_collection.find_one({"_id": ObjectId(pk), "user_email": user_email})
            if not order:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

            # Update the order
            update_data = request.data
            self.orders_collection.update_one(
                {"_id": ObjectId(pk)},
                {"$set": update_data}
            )

            # Fetch the updated order
            updated_order = self.orders_collection.find_one({"_id": ObjectId(pk)})
            updated_order["_id"] = str(updated_order["_id"])  # Convert ObjectId to string
            return Response(updated_order, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid order ID."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete an order for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        try:
            order = self.orders_collection.find_one({"_id": ObjectId(pk), "user_email": user_email})
            if not order:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

            # Delete the order
            self.orders_collection.delete_one({"_id": ObjectId(pk)})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"detail": "Invalid order ID."}, status=status.HTTP_400_BAD_REQUEST)