from datetime import datetime, date
from threading import Lock
from django.shortcuts import render, redirect
from django.http import HttpResponse
from carsharing.models import Car, SharingStation, CarCatalog, \
    Lender, Borrower, ShareInformation, ShareTime
from carsharing import forms
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from carsharing import apps

# global lock for borrow; solving race-condition
borrow_mutex = Lock()


# 성공 시 팝업 표시
# Create your views here.
def index(request):
    upcoming_contract = []

    try:
        upcoming_contract += ShareInformation.objects.filter(
            lender=Lender.objects.get(user=request.user), status__gte=1)
    except:
        pass

    try:
        upcoming_contract += ShareInformation.objects.filter(
            borrower=Borrower.objects.get(user=request.user), status__gte=1)
    except:
        pass

    stations = SharingStation.objects.all()

    context = {
        'stations': stations,
        'contracts': upcoming_contract
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
            form = forms.RegisterUserLenderForm(request.POST)
        elif user_type == 'borrower':
            form = forms.RegisterUserBorrowerForm(request.POST)
        else:
            return HttpResponse('wrong form type')

        if form.is_valid():
            if user_type == 'lender':
                account_no = form.cleaned_data['account_no']

                user_obj = form.save()
                lender_obj = Lender()
                lender_obj.account_no = account_no
                lender_obj.user = user_obj
                lender_obj.save()
            elif user_type == 'borrower':
                card_no = form.cleaned_data['card_no']

                if not apps.check_card_validality(card_no):
                    return HttpResponse('card is not valid')

                user_obj = form.save()
                borrower_obj = Borrower()
                borrower_obj.card_no = card_no
                borrower_obj.user = user_obj
                borrower_obj.save()
            else:
                pass

            # register user completed
            return redirect('login')
        else:
            return HttpResponse('form is not valid')
    else:
        if user_type == "lender":
            form = forms.RegisterUserLenderForm
        elif user_type == "borrower":
            form = forms.RegisterUserBorrowerForm
        else:
            return HttpResponse('wrong form type')

    context = {
        'form': form,
        'user_type': user_type
    }

    return render(request, 'register_user.html', context)


@login_required
def borrow_car_no_param(request):
    return redirect('search_car')


@login_required
def borrow_car(request, car_id):
    if not apps.borrower(request.user):
        context = {
            'error_message': 'lender cannot borrow a car. Please login with borrower.'
        }

        return render(request, 'borrow_car.html', context)

    if request.method == 'POST':
        form = forms.BorrowForm(request.POST)

        if form.is_valid():
            try:
                share_info_obj = ShareInformation.objects.get(car_id=car_id)
            except:
                return render(request, 'borrow_car.html',
                              {
                                  'error_message': 'No such car information at sharinginfo or you already did contract!'
                              })

            borrow_mutex.acquire(1)  # lock acquire1
            if share_info_obj.status == 0:
                share_info_obj.car.available = False
                share_info_obj.car.save()
                share_info_obj.status = 1
                share_info_obj.save()  # 1차 저장
                borrow_mutex.release()  # releasing lock

                # 새로운 쉐어인포 (남은 시간동안 차량 가용)
                share_time_new = ShareTime()
                share_time_new.car_id = car_id
                share_time_new.start_time = datetime.combine(share_info_obj.share_time.start_time, form.cleaned_data['duration'])
                time_duration = datetime.combine(date.min, share_info_obj.share_time.duration) -\
                    datetime.combine(date.min, form.cleaned_data['duration'])
                share_time_new.duration = time_duration.__str__()
                share_time_new.save()

                share_info_obj_new = ShareInformation()
                share_info_obj_new.car_id = car_id
                share_info_obj_new.station_id = share_info_obj.station_id
                share_info_obj_new.status = 0
                share_info_obj_new.lender_id = share_info_obj.lender_id
                share_info_obj_new.share_time = share_time_new
                share_info_obj_new.save()

                # 기존 쉐어인포에 현재 대여중인 정보 입력
                share_time = share_info_obj.share_time
                share_time.duration = form.cleaned_data['duration']
                share_time.save()

                share_info_obj.fee = share_info_obj.car.grade * 5000  # 시간 더하기
                share_info_obj.borrower = Borrower.objects.get(user=request.user)
                share_info_obj.share_time = share_time
                share_info_obj.save()  # 2차 저장
            else:
                borrow_mutex.release()  # releasing mutex
                return HttpResponse('your car choice has been already taken')

            return HttpResponse('successfully borrowed a car!')
        else:
            return HttpResponse('form is not valid')

    share_info_obj = ShareInformation.objects.get(car_id=car_id, status=0)

    context = {
        'form': forms.BorrowForm,
        'station': share_info_obj.station,
        'car': share_info_obj.car,
        'start_time': share_info_obj.share_time.start_time,
        'max_duration': share_info_obj.share_time.duration
    }

    return render(request, 'borrow_car.html', context)


@login_required
def register_car(request):
    if not apps.lender(request.user):
        context = {
            'error_message': 'borrower cannot borrow a car. Please login with lender.'
        }

        return render(request, 'register_car.html', context)

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
            car_obj.owner = Lender.objects.get(user=request.user)
            car_obj.save()

            if station_obj.catalog is None:
                catalog = CarCatalog()
                catalog.cars.add(car_obj)
                catalog.save()
                station_obj.catalog = catalog
            else:
                station_obj.catalog.cars.add(car_obj)

            # dt = form.cleaned_data['start_time']

            share_time_obj = ShareTime()
            share_time_obj.start_time = form.cleaned_data['start_time']  # form.cleaned_data['start_time']
            share_time_obj.duration = form.cleaned_data['duration']
            share_time_obj.car = car_obj
            share_time_obj.save()

            share_info_obj = ShareInformation()
            share_info_obj.car = car_obj
            share_info_obj.share_time = share_time_obj
            share_info_obj.status = 0  # reserved
            share_info_obj.lender = car_obj.owner
            share_info_obj.station = station_obj
            share_info_obj.save()

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


def cancel_contract(request):
    return HttpResponse('not yet implemented')


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
        # 'form': forms.BorrowSearchForm,
        'non_search': True,
        'cars': Car.objects.all().order_by('?')[:10]
    }

    return render(request, 'search_car.html', context)
