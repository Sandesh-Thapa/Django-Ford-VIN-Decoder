from django.urls import path
from .views import index, decodeVin

urlpatterns = [
    path('', index),
    path('<str:vin>/', decodeVin)
]