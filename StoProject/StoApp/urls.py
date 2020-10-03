from django.urls import path
from .views import *


urlpatterns = [
    path('', index),
    path('<str:number>/', CarInfo.as_view(), name='info_number')
]
