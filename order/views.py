from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from user.models import MobileOTP
from inventory.models import Category, Product, Variant
import uuid
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.base import ContentFile

def add_to_cart(user, variant_id, quantity=1):
	try:
		variant = Variant.objects.get(id=variant_id)
	except:
		return 
	try:
		cart = Cart.objects.get(user=user)
	except:
		Cart.objects.create(user=user)
	CartItem.objects.create(
		variant=variant,
		cart=cart,
		quantity=quantity
		)


class CartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
    	try:
    		cart = Cart.objects.get(user=user)
    	except:
    		cart = Cart.objects.create(user=user)
    	data = {}
    	for variant in cart.variants.all():
    		cart_item = CartItem.objects.get(variant=variant, cart=cart)
    		data[variant.id] = {
    			"quantity" : cart_item.quantity
    		}
    	return Response(data)

    def post(self, request):
    	variant_id = request.data.get("variant_id", '')
    	try:
    		cart = Cart.objects.get(user=user)
    	except:
    		cart = Cart.objects.create(user=user)
    	try:
    		variant = cart.variants.get(id=variant_id)
    	except:
    		add_to_cart(request.user, variant_id)
