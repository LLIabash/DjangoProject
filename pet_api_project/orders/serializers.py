from rest_framework import serializers
from .models import Order, OrderItem
from carts.models import Cart  # Предположим, что CartItem - это то, что отражает товары в корзине

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'delivery_address', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        # Если хотите, чтобы корзина очищалась, можете добавить здесь
        # cart_items.delete()  # Убедитесь, что корзина очищается, если нужно

        return order
