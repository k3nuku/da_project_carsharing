from django.shortcuts import render, redirect
from django.http import HttpResponse
from carsharing.forms import SearchForm
from carsharing.models import Car, CarDescription
from carsharing.forms import RegisterCarForm


# Create your views here.
def index(request):
    return render(request, 'index.html')


def borrow_car(request):
    return render(request, 'borrow_car.html')


def register_car(request):
    if request.method == 'POST':
        form = RegisterCarForm(request.POST)

        if form.is_valid():
            desc_obj = CarDescription()
            desc_obj.color = form.color
            desc_obj.submodel = form.submodel
            desc_obj.save()

            car_obj = Car()
            car_obj.description = desc_obj
            car_obj.license_plate = form.license_plate
            car_obj.model = form.model
            car_obj.grade = form.grade
            car_obj.save()

            return render(request, 'index.html', {'message': 'Car information has been successfully registered.'})

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
            return HttpResponse('no such track.')
