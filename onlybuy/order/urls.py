from django.conf.urls import url
from .views import *
urlpatterns = [
    url('^addorder', add_order, name='add_order'),
    url('^orderlist', order_list, name='order_list'),
    url('^cancelorder', cancel_order, name='cancel_order'),
    url('^confirmorder', confirm_order, name='confirm_order'),
    url('^ordergoods', order_goods, name='ordergoods'),
    url('^tomoney', tomoney, name='tomoney'),
    url('^loginfo', logistics_info, name='logistics_info'),
]
