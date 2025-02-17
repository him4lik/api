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
from order.models import CartItem

class ProductCategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {}
        categories = Category.objects.all()
        for category in categories:
            data[category.id] = {
                'category_name': category.name,
                'variants': {var.product.id : var.product.name for var in category.variant_set.all()}
            }
            list(set(variant.product.name for variant in category.variant_set.all()))
        return Response(data)

class ProductFilterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        product_name = request.query_params.get('product', '')
        category = request.query_params.get('category', '')
        title = request.query_params.get('title', '')
        parameters = request.query_params.get('parameters', '')
        variants = Variant.objects.filter(product__name=product_name, categories__name=category)
        var_params = [set(p.parameter for p in var.varparam_set.all()) for var in variants if var.varparam_set.all()]
        var_params = sorted(list(set.intersection(*var_params)))
        filter_opts = {}
        for p in var_params:
            filter_opts[p] = []
            for var in variants:
                try:
                    var_param = var.varparam_set.get(parameter=p)
                    filter_opts[p].append(var_param.value)
                except:
                    continue
        if title:
            variants=variants.filter(title=title)
        if  parameters:
            for k, v in eval(parameters).items():
                variants = variants.filter(varparam__parameter=k,varparam__value__in=v)
        data = {'variants':[], 'filter_opts':filter_opts}
        for var in variants:
            var_params = {p.parameter:p.value for p in var.varparam_set.all()}
            cart_items = CartItem.objects.filter(variant=var, cart__user=request.user) if request.user.is_authenticated else [] 
            data['variants'].append({
                'variant_id': var.id,
                'product':product_name,
                'product_description':var.product.description,
                'category':category,
                'title':var.title,
                'price':var.price, 
                'stock':var.stock_quantity, 
                'parameters':var_params,
                'video':'http://127.0.0.1:8000'+var.file.url if var.file else None,
                'cart_quantity': cart_items.last().quantity if cart_items else 0})
        return Response(data)