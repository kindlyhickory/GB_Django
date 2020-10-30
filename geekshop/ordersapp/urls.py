from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='orders_list'),
    path('create/', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
    path('read/<pk>', ordersapp.OrderRead.as_view(), name='order_read'),
    path('update/<pk>', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    path('delete/<pk>', ordersapp.OrderItemDelete.as_view(), name='order_delete'),
    path('forming/<pk>', ordersapp.order_forming_complete, name='order_forming_complete'),
]
