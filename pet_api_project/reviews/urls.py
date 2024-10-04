from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView

urlpatterns = [
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', ReviewUpdateView.as_view(), name='review-update'),
]