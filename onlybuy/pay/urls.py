from django.conf.urls import url
from .views import *
urlpatterns = [
    # url('^/', , name=''),
    url(r'addbank', addbank, name='addbank'),
    url(r'payorder', payorder, name='payorder'),
]
