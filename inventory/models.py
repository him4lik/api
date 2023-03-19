from django.db import models
from lib.base_classes import BaseModel
from django.contrib.postgres.fields import ArrayField


class Product(BaseModel):
	name = models.CharField(max_length=20)
	parameters = ArrayField(models.CharField(max_length=30), default=list)
	
	def get_product_id(self):
		return ProductChoices[self.name].value

	def __str__(self):
		return self.name

class Category(BaseModel):
	name = models.CharField(max_length=20)

	class Meta:
		verbose_name_plural = "categories"

	def __str__(self):
		return self.name
		
class Variant(BaseModel):
	title = models.CharField(max_length=80, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	price = models.IntegerField()
	stock_quantity = models.IntegerField()
	sold_quantity = models.IntegerField()
	parameters_value = models.JSONField(default=dict, blank=True)
	categories = models.ManyToManyField(Category)
	file = models.FileField(upload_to='videos/', null=True, blank=True)

	def save(self, *args, **kwargs):
		for parameter in self.product.parameters:
			try:
				self.parameters_value[parameter]
			except:
				self.parameters_value[parameter]=''
		super(Variant, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.title)


