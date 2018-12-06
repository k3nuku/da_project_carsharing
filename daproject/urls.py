"""daproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from carsharing import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^admin/', admin.site.urls, name='admin'),
  url(r'^borrow/car', views.borrow_car, name='borrow_car'),
  url(r'^borrow/car/(?P<car_id>\w{0,50})$', views.borrow_car, name='borrow_car_with_id'),
  url(r'^register/car$', views.register_car, name='register_car'),
  url(r'^register/user$', views.register_user_select, name='register_user'),
  url(r'^register/user/(?P<user_type>\w{0,50})$', views.register_user, name='register_user_with_usertype'),
  url(r'^register/station$', views.register_station, name='register_station'),
  url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
  url(r'^logout/$', LogoutView.as_view(next_page='/'), name='logout'),
  path('search/', views.search, name='search')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
