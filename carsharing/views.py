from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'index.html')

def borrow_car(request):
  return render(request, 'borrow_car.html')

def register_car(request):
  return render(requeset, 'register_car.html')