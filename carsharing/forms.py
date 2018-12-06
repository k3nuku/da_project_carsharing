from django import forms
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
    station = forms.ModelChoiceField(queryset=models.SharingStation.objects.all())
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()


class RegisterCatalog(forms.ModelForm):
    class Meta:
        model = models.CarCatalog
        fields = ['cars']


class RegisterStationInfoForm(forms.ModelForm):
    class Meta:
        model = models.SharingStation
        fields = ['name']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        if commit:
            user.save()

        return user
