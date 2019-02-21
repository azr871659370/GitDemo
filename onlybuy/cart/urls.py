from django.conf.urls import url
from .views import *
urlpatterns = [
    url('^addcart', add_cart, name='add_cart'),
    url('^addfavorite', add_favorite, name='add_favorite'),
    url('^deletefavorite', delete_favorite, name='delete_favorite'),
    url('^deletecart', delete_cart, name='delete_cart'),
    url('^changecart', change_cart, name='change_cart'),
    url('^favortocart', favor_to_cart, name='favortocart'),
    url('^cartlist', cart_list, name='cart_list'),
    url('^favorlist', list_favorite, name='favorite_list'),
    url('^buynow', buynow, name='buynow'),
]
