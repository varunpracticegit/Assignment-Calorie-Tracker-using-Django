from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CalorieEntry

# User sign up form class
class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label = 'Confirm Password(again)', widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}

# Update user's data form class
class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_active']
        labels = {'email':'Email'}


class CalorieEntryForm(forms.ModelForm):
    class Meta:
        model = CalorieEntry
        fields = ['food_item', 'quantity', 'calories']


class EditCaloriesForm(forms.ModelForm):
    class Meta:
        model = CalorieEntry
        fields = ['food_item', 'calories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food_item'].widget.attrs.update({'class': 'form-control'})
        self.fields['calories'].widget.attrs.update({'class': 'form-control'})
