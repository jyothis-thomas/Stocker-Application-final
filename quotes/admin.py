from django.contrib import admin
from . models import Stock, TickerModel

admin.site.register(Stock)
admin.site.register(TickerModel)