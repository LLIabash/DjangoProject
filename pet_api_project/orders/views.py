from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Order, OrderItem
from carts.models import Cart, CartItem

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Получаем корзину пользователя
        cart, created = Cart.objects.get_or_create(user=user)

        # Получаем элементы корзины
        cart_items = CartItem.objects.filter(cart=cart)

        # Проверяем, есть ли товары в корзине
        if not cart_items.exists():
            return Response({'error': 'Ваша корзина пуста.'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем входящие данные
        items_data = request.data.get("items")
        if not items_data or not isinstance(items_data, list):
            return Response({'error': 'Не указаны товары для заказа.'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = 0
        for item in items_data:
            product_id = item.get('product')
            quantity = item.get('quantity', 1)

            # Проверяем наличие товара в корзине
            cart_item = cart_items.filter(product_id=product_id).first()
            if not cart_item:
                return Response({'error': f'Товар с ID {product_id} отсутствует в вашей корзине.'}, status=status.HTTP_400_BAD_REQUEST)

            # Учитываем стоимость товара
            total_amount += cart_item.product.price * quantity

        delivery_address = request.data.get("delivery_address")
        if not delivery_address:
            return Response({'error': 'Адрес доставки не указан.'}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем заказ
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            delivery_address=delivery_address
        )

        # Перемещаем товары из корзины в заказ
        for item in items_data:
            product_id = item['product']
            quantity = item['quantity']

            cart_item = cart_items.get(product__id=product_id)
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,  # Используем cart_item для получения экземпляра Product
                quantity=quantity
            )

            # Удаляем товар из корзины
            cart_item.delete()

        return Response({'message': 'Заказ успешно создан.'}, status=status.HTTP_201_CREATED)


