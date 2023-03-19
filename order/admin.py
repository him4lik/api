from django.contrib import admin
from order.models import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)