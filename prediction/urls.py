import django
from django.urls import path
from . import views
#from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="prediction"),
    path('train', views.train, name="train"),
    path('allstocks', views.allstocks, name="allstocks"),

]
