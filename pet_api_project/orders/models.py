from django.conf import settings
from django.db import models
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')  # Возможно, стоит вынести в отдельную модель
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255)

    # Опционально, если хотите добавить метод для удобного отображения
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')  # Уникальное ограничение

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.id}'

