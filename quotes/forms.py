from django import forms
from .models import Stock
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"
class Editprofile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
