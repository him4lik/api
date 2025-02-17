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
from order.models import Cart, CartItem

def modify_cart(user, variant_id, decision, quantity=1):
	try:
		variant = Variant.objects.get(id=variant_id)
	except:
		return 
	try:
		cart = Cart.objects.get(user=user)
	except:
		cart = Cart.objects.create(user=user)
	try:
		cart_item = CartItem.objects.get(
			variant = variant,
			cart=cart,
			)
		if decision == 'increment':
			cart_item.quantity += quantity
		elif decision == 'decrement':
			cart_item.quantity -= quantity
		if cart_item.quantity < 0:
			cart_item.quantity = 0
		cart_item.save()
	except:
		CartItem.objects.create(
			variant=variant,
			cart=cart,
			quantity=quantity
			)

class CartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
    	try:
    		cart = Cart.objects.get(user=request.user)
    	except:
    		cart = Cart.objects.create(user=request.user)
    	data = {}
    	cart_items = CartItem.objects.filter(cart=cart, is_active=True, quantity__gt=0)
    	for cart_item in cart_items:
    		variant = cart_item.variant
    		data[cart_item.id] = {
    			"quantity" : cart_item.quantity,
    			'variant_id': variant.id,
                'product': variant.product.name,
                'title':variant.title,
                'price':variant.price, 
                'stock':variant.stock_quantity, 
                'video':'http://127.0.0.1:8000'+variant.file.url if variant.file else None
    		}
    	return Response(data)

    def post(self, request):
    	variant_id = request.data['variant_id']
    	decision = request.data['decision']
    	modify_cart(request.user, variant_id, decision)
    	data = {'success':True}
    	return Response(data)