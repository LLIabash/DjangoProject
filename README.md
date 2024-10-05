## Описание

Этот пет-проект посвящен созданию API для простого интернет-магазина. Он позволяет пользователям управлять продуктами, корзиной, а также оставлять отзывы.

## Технологии

- Django
- Django REST Framework
- SQLite

## Структура API

API предоставляет следующие конечные точки:

### Пользователи

- GET /api/users/ - [name='user-list'] Получить список всех пользователей.
- POST /api/users/ - [name='user-list-create'] Создать нового пользователя.
- PUT /api/users/<uuid:id>/ - [name='user-list'] Редактировать детали пользователя по его ID.
- GET /api/users/<uuid:id>/ - [name='user-detail'] Получить детали пользователя по его ID.

### Авторизация

- GET /auth/login - [name='login'] Авторизоваться (email;password).

### Продукты

- GET /api/products/ - [name='product-list'] Получить список всех продуктов.
- POST /api/products/ - [name='product-list'] Создать продукт.
- PUT /api/products/<int:pk>/ - [name='product-list'] Редактировать детали продукта по его ID.
- GET /api/products/<int:pk>/ - [name='product-detail'] Получить детали продукта по его ID.

### Корзина

- GET /api/cart/ - [name='cart'] Получить содержимое корзины.
- POST /api/cart/add/ - [name='add-to-cart'] Добавить продукт в корзину.
- POST /api/cart/remove/ - [name='remove-from-cart'] Удалить продукт из корзины.

### Заказы

- POST /api/create-order/ - [name='create_order'] Создать новый заказ.

### Отзывы

- POST /api/reviews/ - [name='review-create'] Оставить новый отзыв о продукте.
- PUT /api/reviews/<int:pk>/ - [name='review-update'] Обновить существующий отзыв по его ID.
