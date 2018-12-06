from django.shortcuts import render, redirect
from django.http import HttpResponse
from carsharing.models import Car, SharingStation, CarCatalog, Lender, Borrower
from carsharing import forms
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from carsharing import apps


# 성공 시 팝업 표시
# Create your views here.
def index(request):
    stations = SharingStation.objects.all()

    context = {
        'stations': stations
    }

    return render(request, 'index.html', context)


def register_user_select(request):
    if request.method == 'POST':
        form = forms.RegisterUserSelectionForm(request.POST)

        if form.is_valid():
            reg_type = form.cleaned_data['reg_type']

            if reg_type == 'reg_lender':
                return redirect('/register/user/lender')
            else:
                return redirect('/register/user/borrower')

    context = {
        'form': forms.RegisterUserSelectionForm
    }

    return render(request, 'register_select_usertype.html', context)


def register_user(request, user_type):
    if request.method == 'POST':
        if user_type == 'lender':
            form = forms.RegistrationLenderForm(request.POST)
        elif user_type == 'borrower':
            form = forms.RegistrationBorrowerForm(request.POST)
        else:
            return HttpResponse('wrong form type')

        if form.is_valid():
            if user_type == 'lender':
                account_no = form.cleaned_data['account_no']

                user_obj = form.save()
                lender_obj = Lender()
                lender_obj.account_no = account_no
                lender_obj.user = user_obj
            elif user_type == 'borrower':
                card_no = form.cleaned_data['card_no']

                if not apps.check_card_validality(card_no):
                    return HttpResponse('card is not valid')

                user_obj = form.save()
                borrower_obj = Borrower()
                borrower_obj.card_no = card_no
                borrower_obj.user = user_obj
            else:
                pass

            # register user completed
            return redirect('login')
        else:
            return HttpResponse('form is not valid')
    else:
        if user_type == "lender":
            form = forms.RegistrationLenderForm
        elif user_type == "borrower":
            form = forms.RegistrationBorrowerForm
        else:
            return HttpResponse('wrong form type')

    context = {
        'form': form,
        'user_type': user_type
    }

    return render(request, 'register_user.html', context)


@login_required
def borrow_car(request):
    if request.method == 'POST':
        pass

    return render(request, 'borrow_car.html')


@login_required
def register_car(request):
    if request.method == 'POST':
        form = forms.RegisterCarForm(request.POST, request.FILES)

        if form.is_valid():
            station_obj = form.cleaned_data['station']

            desc_obj = form.save()

            car_obj = Car()
            car_obj.description = desc_obj
            car_obj.license_plate = form.cleaned_data['license_plate']
            car_obj.model = form.cleaned_data['model']
            car_obj.grade = form.cleaned_data['grade']
            car_obj.save()

            if station_obj.catalog is None:
                catalog = CarCatalog()
                catalog.cars.add(car_obj)
                catalog.save()
                station_obj.catalog = catalog
            else:
                station_obj.catalog.cars.add(car_obj)

            return redirect('index')

    context = {
      'form': forms.RegisterCarForm
    }

    return render(request, 'register_car.html', context)


@staff_member_required
def register_station(request):
    if request.method == 'POST':
        form = forms.RegisterStationInfoForm(request.POST)

        if form.is_valid():
            station = SharingStation.objects.filter(name=form.cleaned_data['name'])

            if station.exists():
                context = {
                    'form': forms.RegisterStationInfoForm,
                    'error': 'station that named is already exist'
                }

                return render(request, 'register_station.html', context)

            catalog = CarCatalog()
            catalog.save()

            station = SharingStation()
            station.name = form.cleaned_data['name']
            #station.location = form.cleaned_data['location']
            station.catalog = catalog
            station.save()

            return redirect('index')

    context = {
        'form': forms.RegisterStationInfoForm
    }

    return render(request, 'register_station.html', context)


def search(request):
    form = forms.SearchForm(request.GET)

    if form.is_valid():
        d1 = Car.objects.filter(model=form.cleaned_data['query'])

        if d1.exists():
            return render(request, 'index.html', {'cars': d1})
        else:
            return HttpResponse('no such car.')
