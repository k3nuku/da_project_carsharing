from django.shortcuts import render, redirect
from django.http import HttpResponse
from carsharing.forms import SearchForm
from carsharing.models import Car, SharingStation, CarCatalog
from carsharing.forms import RegisterCarForm, RegisterStationInfoForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
def index(request):
    stations = SharingStation.objects.all()

    context = {
        'stations': stations
    }

    return render(request, 'index.html', context)


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return HttpResponse('form is not valid')

    context = {
        'form': RegistrationForm
    }

    return render(request, 'register_user.html', context)


@login_required
def borrow_car(request):
    return render(request, 'borrow_car.html')


@login_required
def register_car(request):
    if request.method == 'POST':
        form = RegisterCarForm(request.POST, request.FILES)

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
      'form': RegisterCarForm
    }

    return render(request, 'register_car.html', context)


@staff_member_required
def register_station(request):
    if request.method == 'POST':
        form = RegisterStationInfoForm(request.POST)

        if form.is_valid():
            station = SharingStation.objects.filter(name=form.cleaned_data['name'])

            if station.exists():
                context = {
                    'form': RegisterStationInfoForm,
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
        'form': RegisterStationInfoForm
    }

    return render(request, 'register_station.html', context)


def search(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        d1 = Car.objects.filter(model=form.cleaned_data['query'])

        if d1.exists():
            return render(request, 'index.html', {'cars': d1})
        else:
            return HttpResponse('no such car.')


