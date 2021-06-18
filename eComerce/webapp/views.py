from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import *


#No se crea una api especifica para modificar el stock de un producto
#Se resuelve permitiendo un update parcial
class ProductAPIViewSet(viewsets.ModelViewSet):

	queryset = Product.objects.filter(eliminado=False)
	serializer_class = ProductSerializer
	permission_classes = (IsAuthenticated,)
	http_method_names = ['get', 'post', 'put', 'delete', 'patch']


	def destroy(self, request, *args, **kwargs):
		producto = self.get_object()
		if producto is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		producto.eliminado = True
		producto.save()
		return Response(status=status.HTTP_204_NO_CONTENT)

	def update(self, request, pk=None, *args, **kwargs):
		producto = self.get_object()
		partial = kwargs.pop('partial', False)
		serializer = self.serializer_class(producto, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)


class OrderDetailAPIViewSet(viewsets.ModelViewSet):

	queryset = Order.objects.all()
	serializer_class = OrderDetailSerializer
	permission_classes = (IsAuthenticated,)
	http_method_names = ['get', 'post', 'put', 'delete']

	def destroy(self, request, *args, **kwargs):
		orderdetail = self.get_object()
		if orderdetail is None:
			return Response(status=status.HTTP_404_NOT_FOUND)

		#Se reestablece el stock del producto
		producto = ProductSerializer()
		producto = request.data.get('producto')
		p = Producto.objects.get(id=producto.get("id"))
		p.stock += orderdetail.quantity
		p.save()

		orderdetail.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class OrderAPIViewSet(viewsets.ModelViewSet):

	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = (IsAuthenticated,)
	http_method_names = ['get', 'post', 'put', 'delete']

	def destroy(self, request, *args, **kwargs):
		order = self.get_object()
		if order is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		orderdetails = request.data.get('orderdetail')
		for od in orderdetails:
			od_serializer = OrderDetailAPIViewSet.serializer_class(data=od)
			od_serializer.delete()

		order.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	#esta solo pq para debugear me ayudaba
	def create(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=False)
		serializer.save()
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

"""
	def get_total(self):
		order = self.get_object()
		#order = Order.objects.filter(id=order.id, **query_params)
		q = OrderDetail.filter(order=order.id)

    	total = q.aggregate(Sum('quantity'))['quantity']
"""
