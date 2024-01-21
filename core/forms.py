from django import forms
from django.contrib.auth.models import User
from .models import Product, UserProfile
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.forms.widgets import PasswordInput, TextInput, SelectDateWidget, Textarea, RadioSelect, NumberInput
from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from django.forms import ModelForm
from django.views.generic import View

class ProductForm(forms.ModelForm):

    SERVING_CHOICES = ((0.0,'0'),(1.0,'1'),(2.0,'2'),(3.0,'3'),(4.0,'4'),)

    servings = forms.FloatField(widget=forms.Select(attrs={'class':'form-control','placeholder': 'Project'},
    	choices=SERVING_CHOICES,
    	),
    )

    class Meta:
        model = Product
        fields = ['servings']


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
    email = forms.EmailField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Email'}),max_length=75)
    email_confirm = forms.EmailField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Confirm Email'}),max_length=75, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'email_confirm', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(self.cleaned_data['password'])
        return password

    def clean_email_confirm(self):
        print(self.cleaned_data)
        email = self.cleaned_data.get('email')
        email_confirm = self.cleaned_data.get('email_confirm')
        if email != email_confirm:
            raise forms.ValidationError("Whops!.. XD.. emails must match")

        email_exists = User.objects.filter(email=email)
        if email_exists.exists():
            raise forms.ValidationError("Whops! This email already exists")

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password',}))

class EditProfileForm(UserChangeForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
    email = forms.EmailField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Email'}),max_length=75)

    class Meta:
        model = User
        fields = {'username','email', 'password'}

class UpdateProfileForm(ModelForm):
    phone = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'phone'}),max_length=500)

    class Meta:
        model = UserProfile
        fields = {'phone'}
