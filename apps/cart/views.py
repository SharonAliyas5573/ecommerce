from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.authentication.permissions import IsAdminOrCustomer
from apps.authentication.authentication import JWTAuthentication
from bson.objectid import ObjectId
from ecommerce.settings import mongo_db


class CartViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrCustomer]

    carts_collection = mongo_db['carts']
    products_collection = mongo_db['products']

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the cart for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        try:
            cart = self.carts_collection.find_one({"user_email": user_email})
            if not cart:
                # Create a new cart if it doesn't exist
                cart = {"user_email": user_email, "cart_items": []}
                self.carts_collection.insert_one(cart)

            cart["_id"] = str(cart["_id"])  # Convert ObjectId to string
            return Response(cart, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def add_item(self, request, *args, **kwargs):
        """
        Add an item to the cart for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        item_data = request.data

        if not item_data.get("product_id") or not item_data.get("quantity"):
            return Response({"error": "Product ID and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(item_data["quantity"], int) or item_data["quantity"] <= 0:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validate product existence
            product = self.products_collection.find_one({"_id": ObjectId(item_data["product_id"])})
            if not product:
                return Response({"error": "Invalid product ID."}, status=status.HTTP_400_BAD_REQUEST)

            cart = self.carts_collection.find_one({"user_email": user_email})
            if not cart:
                # Create a new cart if it doesn't exist
                cart = {"user_email": user_email, "cart_items": []}
                self.carts_collection.insert_one(cart)

            # Check if the item already exists in the cart
            for item in cart["cart_items"]:
                if item["product_id"] == item_data["product_id"]:
                    item["quantity"] += item_data["quantity"]
                    break
            else:
                # Add the new item to the cart
                cart["cart_items"].append(item_data)

            # Update the cart in the database
            self.carts_collection.update_one(
                {"_id": cart["_id"]},
                {"$set": {"cart_items": cart["cart_items"]}}
            )

            cart["_id"] = str(cart["_id"])  # Convert ObjectId to string
            return Response(cart, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def remove_item(self, request, pk=None, *args, **kwargs):
        """
        Remove an item from the cart for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        try:
            cart = self.carts_collection.find_one({"user_email": user_email})
            if not cart:
                return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the item exists in the cart
            item_exists = any(item["product_id"] == pk for item in cart["cart_items"])
            if not item_exists:
                return Response({"error": "Item not found in the cart."}, status=status.HTTP_404_NOT_FOUND)

            # Remove the item from the cart
            cart["cart_items"] = [item for item in cart["cart_items"] if item["product_id"] != pk]

            # Update the cart in the database
            self.carts_collection.update_one(
                {"_id": cart["_id"]},
                {"$set": {"cart_items": cart["cart_items"]}}
            )

            cart["_id"] = str(cart["_id"])  # Convert ObjectId to string
            return Response(cart, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def clear_cart(self, request, *args, **kwargs):
        """
        Clear all items from the cart for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        try:
            cart = self.carts_collection.find_one({"user_email": user_email})
            if not cart:
                return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

            # Clear the cart items
            cart["cart_items"] = []

            # Update the cart in the database
            self.carts_collection.update_one(
                {"_id": cart["_id"]},
                {"$set": {"cart_items": []}}
            )

            cart["_id"] = str(cart["_id"])  # Convert ObjectId to string
            return Response(cart, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)