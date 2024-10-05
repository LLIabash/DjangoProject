from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Product
from reviews.models import Review

User = get_user_model()


class ReviewTests(APITestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        # Создаем продукт
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.99,
            quantity=100
        )

        # URL для создания и обновления отзывов
        self.create_url = reverse('review-create')
        self.update_url = reverse('review-update', args=[self.product.id])

    def test_create_review(self):
        data = {
            'product': self.product.id,
            'rating': 5,
            'comment': 'Great product!'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.get()
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great product!')

    def test_update_review(self):
        # Создаем отзыв
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment='Good product.'
        )

        # Данные для обновления, включая обязательное поле product
        data = {
            'product': review.product.id,  # Обязательно указываем ID продукта
            'rating': 3,
            'comment': 'Average product.'
        }

        response = self.client.put(reverse('review-update', args=[review.id]), data)

        # Логируем ответ для отладки
        print(response.data)  # Выводим ошибку из ответа, если есть

        # Проверяем статус ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Обновляем данные из базы и проверяем их
        review.refresh_from_db()
        self.assertEqual(review.rating, 3)
        self.assertEqual(review.comment, 'Average product.')