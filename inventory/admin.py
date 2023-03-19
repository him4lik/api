from django.contrib import admin
from .models import Product, Variant, Category

admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Category)