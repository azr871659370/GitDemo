from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderGoods)
admin.site.register(Logistics)
admin.site.register(LogisticsInfo)