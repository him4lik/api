from django.urls import path, include
from order import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
]
