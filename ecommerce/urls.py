from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.authentication.urls')),
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('discounts/', include('apps.discounts.urls')),
]