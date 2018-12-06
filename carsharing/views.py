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
    if request.method == 'GET':
        return redirect('search_car')

    return HttpResponse('not implemented yet!')


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


def search_car(request):
    if request.method == 'GET':
        form = forms.BorrowSearchForm(request.GET)
    else:
        form = forms.BorrowSearchForm(request.POST)

    if form.is_valid():
        query = form.cleaned_data['query']

        car_model_q = car_grade_q = car_license_q = car_color_q \
            = car_sub_model_q = station_name_q = None

        try:
            car_model_q = Car.objects.filter(model__contains=query, available=True)
        except ValueError:
            pass  # perform semi full-text searching

        try:
            car_grade_q = Car.objects.filter(grade__lte=query, available=True)
        except ValueError:
            pass

        try:
            car_license_q = Car.objects.filter(license_plate__contains=query, available=True)
        except ValueError:
            pass

        try:
            car_color_q = Car.objects.filter(description__color__contains=query, available=True)
        except ValueError:
            pass

        try:
            car_sub_model_q = Car.objects.filter(description__sub_model__contains=query, available=True)
        except ValueError:
            pass

        try:
            station_name_q = SharingStation.objects.filter(name__contains=query, catalog__cars__available=True)
        except ValueError:
            pass

            # station_location_q = SharingStation.objects.filter(location__contains=query)

        search_result = (
            car_model_q if car_model_q is not None else None,
            car_grade_q if car_grade_q is not None else None,
            car_license_q if car_license_q is not None else None,
            car_color_q if car_color_q is not None else None,
            car_sub_model_q if car_sub_model_q is not None else None,
            station_name_q if station_name_q is not None else None
        )

        sr = list(set(list(filter(None, search_result))))

        context = {
            'form': forms.BorrowSearchForm,
            'search_data': sr,
            'non_search': False
        }

        return render(request, 'search_car.html', context)

    context = {
        'form': forms.BorrowSearchForm,
        'non_search': True,
        'cars': Car.objects.all().order_by('?')[:10]
    }

    return render(request, 'search_car.html', context)
