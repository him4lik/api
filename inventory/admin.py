from django.contrib import admin
from .models import Product, Variant, Category, VarParam

class VarParamAdmin(admin.ModelAdmin):
	list_display = ('variant', 'parameter', 'value')

admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Category)
admin.site.register(VarParam, VarParamAdmin)