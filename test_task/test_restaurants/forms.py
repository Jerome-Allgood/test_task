from django import forms
from django.contrib.auth.models import User

from .models import CustomUser, Restaurant


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'})
        }


class RestaurantForm(forms.Form):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(),
                                        widget=forms.Select(
                                            attrs={'class': 'form-control'}))


class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter phone'}))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
