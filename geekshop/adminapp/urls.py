from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.UsersCreateView.as_view(), name='user_create'),
    path('users/read/', adminapp.UsersListView.as_view(), name='users'),
    path('users/update/<pk>/', adminapp.UsersUpdateView.as_view(), name='user_update'),
    path('users/delete/<pk>/', adminapp.UsersDeleteView.as_view(), name='user_delete'),

    path('categories/create/', adminapp.CategoriesCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.CategoriesListView.as_view(), name='categories'),
    path('categories/update/<pk>/', adminapp.CategoriesUpdateView.as_view(), name='category_update'),
    path('categories/delete/<pk>/', adminapp.CategoriesDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<pk>/', adminapp.ProductsCreateView.as_view(), name='product_create'),
    path('products/read/category/<pk>/', adminapp.ProductsListView.as_view(), name='products'),
    path('products/read/<pk>/', adminapp.ProductListView.as_view(), name='product_read'),
    path('products/update/<pk>/', adminapp.ProductsEditView.as_view(), name='product_update'),
    path('products/delete/<pk>/', adminapp.ProductsDeleteView.as_view(), name='product_delete'),

    path('orders/read/', adminapp.OrdersListView.as_view(), name='orders_read'),
    path('orders/read/<status>/<pk>/', adminapp.order_change_status, name='order_change_status'),

]
