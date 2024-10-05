from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from products.models import Product
from .models import Cart, CartItem

class CartTests(APITestCase):
    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)

        # Создание тестового продукта
        self.product = Product.objects.create(name='Test Product', price=10.0, quantity=200)

    def test_get_cart(self):
        # Проверка, что корзина создается для пользователя
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_add_to_cart(self):
        # Добавление товара в корзину
        response = self.client.post(reverse('add-to-cart'), {
            'product_id': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(response.data['quantity']), 2)

        # Проверка, что товар действительно добавился в корзину
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_from_cart(self):
        # Сначала добавляем товар в корзину
        self.client.post(reverse('add-to-cart'), {
            'product_id': self.product.id,
            'quantity': 1
        })

        # Удаление товара из корзины
        response = self.client.delete(reverse('remove-from-cart'), {
            'product_id': self.product.id
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка, что товар удален из корзины
        cart = Cart.objects.get(user=self.user)
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(cart=cart, product=self.product)

