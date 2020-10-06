from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='basket'),
    path('add/<pk>/', basketapp.basket_add, name='basket_add'),
    path('delete/<pk>/', basketapp.basket_delete, name='basket_delete')
]
