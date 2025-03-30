from django.urls import path
from .views import DiscountViewSet

urlpatterns = [
    path('', DiscountViewSet.as_view({'get': 'list', 'post': 'create'}), name='discount-list-create'),
    path('<str:pk>/', DiscountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='discount-detail'),
]