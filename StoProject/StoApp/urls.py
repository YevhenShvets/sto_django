from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('create/car', CarCreate.as_view(), name='create_car'),
    path('<str:number>/create_repair/', RepairCreate.as_view(), name='create_repair'),
    path('<str:number>/', CarInfo.as_view(), name='info_number')

]
