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

class ProductCategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {}
        categories = Category.objects.all()
        for category in categories:
            data[category.name] = list(set(variant.product.name for variant in category.variant_set.all()))
        return Response(data)

class ProductFilterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        product_name = request.query_params.get('product', None)
        category = request.query_params.get('category', None)
        parameters = request.query_params.get('parameters', None)
        title = request.query_params.get('title', None)
        variants = Variant.objects.filter(product__name=product_name, categories__name=category)
        if parameters:
            variants=variants.filter(parameters_value=eval(parameters.replace("'", "\"")))
        if title:
            variants=variants.filter(title=title)
        data = []
        for var in variants:
            data.append({
                'product':product_name,
                'category':category,
                'title':var.title,
                'price':var.price, 
                'stock':var.stock_quantity, 
                'parameters':var.parameters_value,
                'video':'http://127.0.0.1:8000'+var.file.url})
        return Response(data)

    def post(self, request):
        request_id = request.data['request_id']
        otp = request.data['otp']
        res = verify_otp(request_id, otp)
        if res:
            return Response(res['text'], status=res['status'])

        otp = MobileOTP.objects.get(request_id=request_id)
        flag = False
        user_obj = get_user(otp.username, True)
        refresh = RefreshToken.for_user(user_obj)
        print(refresh)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })