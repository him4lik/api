from django.db import models
from django.contrib.auth.models import User
from lib.base_classes import BaseModel
import random
from inventory.models import Variant

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variants = models.ManyToManyField(Variant, blank=True, related_name='carts', through='CartItem')

    def __str__(self):
    	return str(self.user.username)

class CartItem(BaseModel):
	variant = models.OneToOneField(Variant, on_delete=models.CASCADE)
	cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
	quantity = models.IntegerField()

	def __str__(self):
		return f"{self.cart.user.username}-{self.variant.title}"


