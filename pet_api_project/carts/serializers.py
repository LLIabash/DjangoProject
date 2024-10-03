from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']  # добавьте все поля, которые хотите вернуть

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Здесь используем ProductSerializer

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(many=True, source='cartitem_set')  # Используем related_name по умолчанию

    class Meta:
        model = Cart
        fields = ['user', 'products']  # Убедитесь, что это 'products'