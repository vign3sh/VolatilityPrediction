import django
from django.urls import path
from . import views
#from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="stockprice"),
    path('values', views.values, name="stockprice-values"),

]
