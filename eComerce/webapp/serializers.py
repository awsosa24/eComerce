from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from .models import *


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = [
			"id",
			"name",
			"price",
			"stock"
		]


class OrderDetailSerializer(serializers.ModelSerializer):
	order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
	#product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
	class Meta:
		model = OrderDetail
		fields = [
			"id",
			"quantity",
			"order",
			"product"
		]

			# Cada orden en OrderDetail solo puede tener una vez cada producto
		"""
		validators = [
			UniqueTogetherValidator(
				queryset=OrderDetail.objects.all(),
				fields=['order', 'product']
			)
		]
		"""

	def validate(self, data):
		# Se valida que exista stock y que se pida almenos una unidad
		producto = get_object_or_404(Product, id=data["product"].id)
		if data["quantity"] > producto.stock:
			raise serializers.ValidationError("No hay stock.")
		elif data["quantity"] < 0:
			raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
		return data

	def create(order, validated_data):
		producto = ProductSerializer()
		producto = validated_data.get('product')
		quantity = validated_data.get('quantity')
		#creo el objeto
		#por alguna razon no me toma si le paso **validated_data
		orderdetail = OrderDetail.objects.create(order=order, quantity=quantity, product=producto)
		orderdetail.save()
		#Se trae el producto y se actualiza
		p = Product.objects.get(id=producto.id)
		p.stock -= orderdetail.quantity
		p.save()
		print("create od fin")
		return orderdetail

	def update(self, instance, validated_data):
		print("update")
		producto = ProductSerializer()
		#Se asume que solo se puede cambiar la cantidad
		cantidadinicial = instance.quantity
		instance.quantity = validated_data.get('quantity', instance.quantity)
		instance.save()
		cantidadfinal = instance.quantity - cantidadinicial
		#Se trae el producto y se actualiza
		producto = validated_data.get('producto')
		p = Product.objects.get(id=producto.get("id"))
		p.stock -= cantidadfinal
		p.save()

		return instance


class OrderSerializer(serializers.ModelSerializer):
	orderdetails = OrderDetailSerializer(many=True,required=False)

	class Meta:
		model = Order
		fields = [
			"id",
			"date_time",
			"orderdetails"
		]

	def create(self, validated_data):
		orderdetails = validated_data.pop('orderdetails', [])
		order = Order.objects.create(**validated_data)
		for od in orderdetails:
			#OrderDetail.objects.create(order=order, **od)
			OrderDetailSerializer.create(order=order, validated_data=od)
		return order

	def update(self, instance, validated_data):
		orderdetails = validated_data.pop('orderdetails', [])
		instance.date_time = validated_data.get('date_time', instance.date_time)
		instance.save()
		for od in orderdetails:
			OrderDetail.objects.update(order=instance, **od)
		return instance
