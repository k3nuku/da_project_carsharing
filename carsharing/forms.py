from django import forms
from colorfield.fields import ColorField
from carsharing import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SearchForm(forms.Form):
    query = forms.CharField(required=True)


class RegisterCarForm(forms.Form):
    color = forms.CharField(max_length=10)
    submodel = forms.CharField(max_length=50)
    model = forms.CharField(max_length=100)
    grade = forms.DecimalField(decimal_places=1, max_digits=1)
    license_plate = forms.CharField(max_length=100)
