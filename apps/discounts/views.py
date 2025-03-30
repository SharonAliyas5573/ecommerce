from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.authentication.authentication import JWTAuthentication
from apps.authentication.permissions import IsAdminOrCustomer
from bson.objectid import ObjectId
from ecommerce.settings import mongo_db


class DiscountViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    discounts_collection = mongo_db['discounts']

    def list(self, request):
        """
        Retrieve all discounts for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        discounts = list(self.discounts_collection.find({"user_email": user_email}))

        # Convert ObjectId to string
        for discount in discounts:
            discount["_id"] = str(discount["_id"])

        return Response(discounts, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new discount for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        discount_data = request.data

        # Validate required fields
        if not discount_data.get("code") or not discount_data.get("percentage") or not discount_data.get("valid_from") or not discount_data.get("valid_to"):
            return Response({"error": "All fields (code, percentage, valid_from, valid_to) are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the discount code already exists for the user
        existing_discount = self.discounts_collection.find_one({"user_email": user_email, "code": discount_data["code"]})
        if existing_discount:
            return Response({"error": "Discount code already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Add user_email to the discount data
        discount_data["user_email"] = user_email
        discount_data["active"] = discount_data.get("active", True)  # Default to active if not provided

        # Insert the discount into the database
        result = self.discounts_collection.insert_one(discount_data)
        discount_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string

        return Response(discount_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific discount by ID for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        try:
            discount = self.discounts_collection.find_one({"_id": ObjectId(pk), "user_email": user_email})
            if not discount:
                return Response({"error": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)

            discount["_id"] = str(discount["_id"])  # Convert ObjectId to string
            return Response(discount, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid discount ID."}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update a discount for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        try:
            discount = self.discounts_collection.find_one({"_id": ObjectId(pk), "user_email": user_email})
            if not discount:
                return Response({"error": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)

            # Update the discount
            update_data = request.data
            self.discounts_collection.update_one(
                {"_id": ObjectId(pk)},
                {"$set": update_data}
            )

            # Fetch the updated discount
            updated_discount = self.discounts_collection.find_one({"_id": ObjectId(pk)})
            updated_discount["_id"] = str(updated_discount["_id"])  # Convert ObjectId to string
            return Response(updated_discount, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid discount ID."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete a discount for the authenticated user.
        """
        user_email = request.user.email  # Use dot notation
        try:
            discount = self.discounts_collection.find_one({"_id": ObjectId(pk), "user_email": user_email})
            if not discount:
                return Response({"error": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)

            # Delete the discount
            self.discounts_collection.delete_one({"_id": ObjectId(pk)})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"error": "Invalid discount ID."}, status=status.HTTP_400_BAD_REQUEST)