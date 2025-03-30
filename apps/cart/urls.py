from django.urls import path
from .views import CartViewSet

urlpatterns = [
    path('', CartViewSet.as_view({'get': 'retrieve'}), name='cart-retrieve'),
    path('add_item/', CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),
    path('remove_item/<str:pk>/', CartViewSet.as_view({'delete': 'remove_item'}), name='cart-remove-item'),
    path('clear_cart/', CartViewSet.as_view({'post': 'clear_cart'}), name='cart-clear-cart'),
]