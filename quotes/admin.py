from django.contrib import admin
from . models import Stock, TickerModel

class Stock_list(admin.ModelAdmin):
    list_display = ('ticker', 'user')   

class TickerModel_list(admin.ModelAdmin):
    list_display = ('company_name', 'ticker_symbols')
    search_fields = ['ticker_symbols']

admin.site.register(Stock,Stock_list)
admin.site.register(TickerModel, TickerModel_list)