# from django.contrib.auth.models import User
import json
# from django.utils import timezone
# from django.core.files import File
from quotes.models import TickerModel
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create ticker'

    def handle(self, *args, **kwargs):
        with open('symbol.txt') as json_file:
            data = json.load(json_file)
            for p in data:
                ticker_object = TickerModel(company_name = p['name'], ticker_symbols = p['symbol'])
                print(ticker_object.company_name)
                print(ticker_object.ticker_symbols)
                ticker_object.save()
            print("sucess")