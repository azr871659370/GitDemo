from django.conf.urls import url
from .views import *
urlpatterns = [
    # url('^/', , name=''),
    url('aa', aa),
    url('goodlist', goodlist, name='goodlst'),
    url('goodetail', goodetail, name='goodetail'),
    url('search', search, name='search'),
]
