from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from users.models import User
from products.models import Product


class CartView(APIView):
    def get(self, request):
        user = request.user  # Убедитесь, что это объект User
        cart, created = Cart.objects.get_or_create(user=user)  # user должен быть экземпляром User
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # Увеличиваем количество, если продукт уже в корзине
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # Устанавливаем количество в случае добавления нового товара
            cart_item.quantity = quantity
            cart_item.save()

        return Response({'message': 'Product added to cart', 'quantity': cart_item.quantity},
                        status=status.HTTP_201_CREATED)


class RemoveFromCartView(APIView):
    def delete(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        product_id = request.data.get('product_id')

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()

        return Response({'message': 'Product removed from cart'}, status=status.HTTP_204_NO_CONTENT)