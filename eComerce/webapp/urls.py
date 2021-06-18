from django.conf.urls import url, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register(r'product', ProductAPIViewSet)
router.register(r'order', OrderAPIViewSet)
router.register(r'orderdetail', OrderDetailAPIViewSet)

app_name = "webapp"

urlpatterns = [
    url(r'^', include(router.urls)),

]
