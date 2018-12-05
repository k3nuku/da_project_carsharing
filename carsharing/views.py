from django.shortcuts import render, redirect
from django.http import HttpResponse
from carsharing.forms import SearchForm
from carsharing.models import Car, CarDescription
from carsharing.forms import RegisterCarForm


# Create your views here.
def index(request):
    cars = Car.objects.all()

    context = {
        'cars': cars
    }

    return render(request, 'index.html', context)


def borrow_car(request):
    return render(request, 'borrow_car.html')


def register_car(request):
    if request.method == 'POST':
        form = RegisterCarForm(request.POST, request.FILES)

        if form.is_valid():
            desc_obj = form.save()

            car_obj = Car()
            car_obj.description = desc_obj
            car_obj.license_plate = form.cleaned_data['license_plate']
            car_obj.model = form.cleaned_data['model']
            car_obj.grade = form.cleaned_data['grade']
            car_obj.save()

            return redirect('index')

    context = {
      'form': RegisterCarForm
    }

    return render(request, 'register_car.html', context)


def search(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        d1 = Car.objects.filter(model=form.cleaned_data['query'])

        if d1.exists():
            return render(request, 'index.html', {'cars': d1})
        else:
            return HttpResponse('no such car.')
