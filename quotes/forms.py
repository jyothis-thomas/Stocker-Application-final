from django import forms
from .models import Stock
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"

class Editprofile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        users_emails = [ x.email for x in User.objects.all().only("email")]
        user_entered_email = self.cleaned_data['email']
        if user_entered_email in users_emails:
            raise ValidationError(gettext("Duplicate email"),code='email_already_exists')
        return user_entered_email

    def __init__(self, *args, **kwargs):
        super(Editprofile, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        