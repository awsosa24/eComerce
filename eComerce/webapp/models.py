from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):

	date_time = models.DateTimeField(auto_now_add=True)


class Product(models.Model):

	name = models.CharField(max_length=64)
	price = models.FloatField(default=0, blank=True)
	stock = models.IntegerField(default=0, blank=True)
	#No lo especifica el ejercicio, no querran borrado logico?
	eliminado = models.BooleanField(blank=True, default=False)	


class OrderDetail(models.Model):

	order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name="order")
	quantity = models.IntegerField()
	product = models.ForeignKey(Product, null=True, on_delete=models.PROTECT, related_name="product")
