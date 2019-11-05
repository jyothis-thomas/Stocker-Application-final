from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext

class UserRegForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    class Meta:
        model = User
        fields =['first_name','last_name','username','email','password1','password2']
    def clean_email(self):
        users_emails = [ x.email for x in User.objects.all().only("email")]
        user_entered_email = self.cleaned_data['email']
        if user_entered_email in users_emails:
            raise ValidationError(gettext("Duplicate email"),code='email_already_exists')
        return user_entered_email