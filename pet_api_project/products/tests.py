from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product

class ProductTests(APITestCase):

    def setUp(self):
        # Создаем два тестовых продукта
        self.product1 = Product.objects.create(
            name="Product 1",
            description="Description 1",
            price=100.00,
            quantity=10
        )
        self.product2 = Product.objects.create(
            name="Product 2",
            description="Description 2",
            price=200.00,
            quantity=5
        )
        self.list_create_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product1.pk})

    def test_get_products(self):
        # Тестирование получения списка всех продуктов
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_product(self):
        # Тестирование создания нового продукта
        data = {
            'name': 'Product 3',
            'description': 'Description 3',
            'price': 300.00,
            'quantity': 20
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)

    def test_create_product_invalid_data(self):
        # Тестирование создания продукта с некорректными данными
        data = {
            'name': '',
            'description': 'Description 4',
            'price': 'invalid price',  # Некорректное значение цены
            'quantity': 10
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_product_detail(self):
        # Тестирование получения деталей конкретного продукта
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_update_product(self):
        # Тестирование обновления продукта
        data = {'name': 'Updated Product 1'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Updated Product 1')

    def test_delete_product(self):
        # Тестирование удаления продукта
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)
