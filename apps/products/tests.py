from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Category

class ProductTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product_data = {
            'name': 'Smartphone',
            'description': 'Latest model smartphone',
            'price': 699.99,
            'stock': 50,
            'category': self.category.id,
            'image': 'path/to/image.jpg'
        }
        self.product = Product.objects.create(**self.product_data)

    def test_create_product(self):
        response = self.client.post(reverse('product-list'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_product(self):
        response = self.client.get(reverse('product-detail', args=[self.product.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product(self):
        updated_data = {
            'name': 'Updated Smartphone',
            'description': 'Updated description',
            'price': 599.99,
            'stock': 30,
            'category': self.category.id,
            'image': 'path/to/new_image.jpg'
        }
        response = self.client.put(reverse('product-detail', args=[self.product.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Smartphone')

    def test_delete_product(self):
        response = self.client.delete(reverse('product-detail', args=[self.product.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)