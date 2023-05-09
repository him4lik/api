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
    	pass