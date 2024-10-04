from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('api/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/', include('carts.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('reviews.urls')),
]
