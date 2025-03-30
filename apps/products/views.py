from rest_framework import viewsets, status
from rest_framework.response import Response
from bson.objectid import ObjectId
from django.core.cache import cache 
from ecommerce.settings import mongo_db
from apps.authentication.authentication import JWTAuthentication

class ProductViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    products_collection = mongo_db['products']

    def create(self, request, *args, **kwargs):
        """
        Create a new product in the MongoDB collection.
        """
        product_data = request.data
        result = self.products_collection.insert_one(product_data)
        product_data["_id"] = str(result.inserted_id)
        return Response(product_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update an existing product in the MongoDB collection.
        """
        product_id = kwargs.get("pk")
        product_data = request.data

        if not ObjectId.is_valid(product_id):
            return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)

        result = self.products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product_data}
        )

        if result.matched_count == 0:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product_data["_id"] = product_id
        return Response(product_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a product from the MongoDB collection.
        """
        product_id = kwargs.get("pk")

        if not ObjectId.is_valid(product_id):
            return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)

        result = self.products_collection.delete_one({"_id": ObjectId(product_id)})

        if result.deleted_count == 0:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all products from the MongoDB collection with Redis caching.
        """
        cache_key = "products_list"
        cached_products = cache.get(cache_key)

        if cached_products:
            return Response(cached_products, status=status.HTTP_200_OK)

        products = list(self.products_collection.find())
        for product in products:
            product["_id"] = str(product["_id"])  # Convert ObjectId to string

        # Cache the products for 5 minutes
        cache.set(cache_key, products, timeout=300)
        return Response(products, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single product by ID from the MongoDB collection with Redis caching.
        """
        product_id = kwargs.get("pk")
        cache_key = f"product_{product_id}"

        if not ObjectId.is_valid(product_id):
            return Response({"error": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)

        cached_product = cache.get(cache_key)
        if cached_product:
            return Response(cached_product, status=status.HTTP_200_OK)

        product = self.products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product["_id"] = str(product["_id"])  # Convert ObjectId to string

        # Cache the product for 5 minutes
        cache.set(cache_key, product, timeout=300)
        return Response(product, status=status.HTTP_200_OK)