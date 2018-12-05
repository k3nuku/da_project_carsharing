from django import forms
from colorfield.fields import ColorField
from carsharing import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SearchForm(forms.Form):
    query = forms.CharField(required=True)


class RegisterCarForm(forms.ModelForm):
    class Meta:
        model = models.CarDescription
        fields = ['color', 'submodel', 'photo']

    model = forms.CharField(max_length=100)
    grade = forms.IntegerField()
    license_plate = forms.CharField(max_length=100)
