from django.urls import path, include
from inventory import views

urlpatterns = [
    path('product-category/', views.ProductCategoryView.as_view(), name='product-category'),
    path('browse/', views.ProductFilterView.as_view(), name='product-filter'),
]
