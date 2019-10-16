from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    class Meta:
        unique_together = (('ticker', 'user'),)
    ticker = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    def __str__(self):
        return self.ticker

class TickerModel(models.Model):
    company_name = models.TextField()
    ticker_symbols = models.CharField(max_length=10, primary_key = True)