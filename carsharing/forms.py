from django import forms
from carsharing import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetimewidget.widgets import DateTimeWidget


class SearchForm(forms.Form):
    query = forms.CharField(required=True)


class RegisterCarForm(forms.ModelForm):
    class Meta:
        model = models.CarDescription
        fields = ['color', 'sub_model', 'photo']

    model = forms.CharField(max_length=100)
    grade = forms.IntegerField()
    license_plate = forms.CharField(max_length=100)
    station = forms.ModelChoiceField(queryset=models.SharingStation.objects.all())

    start_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],
                                     widget=forms.TextInput(
                                     attrs={'placeholder': 'YYYY-m-d H:M'}))

    duration = forms.TimeField(widget=forms.TextInput(
                               attrs={'placeholder': 'H:M'}))


class RegisterUserSelectionForm(forms.Form):
    reg_type = forms.ChoiceField(
        choices=[('reg_lender', 'Lender'), ('reg_borrower', 'Borrower')],
        widget=forms.RadioSelect()
    )


class RegisterCatalog(forms.ModelForm):
    class Meta:
        model = models.CarCatalog
        fields = ['cars']


class RegisterStationInfoForm(forms.ModelForm):
    class Meta:
        model = models.SharingStation
        fields = ['name']


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)

        if commit:
            user.save()

        return user


class RegisterUserLenderForm(RegisterUserForm):
    account_no = forms.CharField(max_length=100)


class RegisterUserBorrowerForm(RegisterUserForm):
    card_no = forms.CharField(max_length=100)


class BorrowSearchForm(forms.Form):
    query = forms.CharField(max_length=250)
    start_time = forms.DateTimeField(required=False)
    duration = forms.TimeField(required=False)


class BorrowForm(forms.Form):
    start_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],
                                     widget=forms.TextInput(
                                     attrs={'placeholder': 'YYYY-m-d H:M'}))

    duration = forms.TimeField(widget=forms.TextInput(
                               attrs={'placeholder': 'H:M'}))
