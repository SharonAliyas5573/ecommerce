from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Cart, CartItem
from apps.authentication.models import User

class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.cart = Cart.objects.create(user=self.user)

    def test_add_item_to_cart(self):
        response = self.client.post(reverse('cart:add_item'), {'product_id': 1, 'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_remove_item_from_cart(self):
        item = CartItem.objects.create(cart=self.cart, product_id=1, quantity=2)
        response = self.client.delete(reverse('cart:remove_item', args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_get_cart_items(self):
        CartItem.objects.create(cart=self.cart, product_id=1, quantity=2)
        response = self.client.get(reverse('cart:list_items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cart_persistence(self):
        self.client.post(reverse('cart:add_item'), {'product_id': 1, 'quantity': 2})
        self.client.logout()
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('cart:list_items'))
        self.assertEqual(len(response.data), 1)