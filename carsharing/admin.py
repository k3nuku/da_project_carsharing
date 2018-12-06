from django.contrib import admin
from carsharing.models import Car, SharingStation, ShareInformation

# Register your models here.
admin.site.register(Car)
admin.site.register(SharingStation)
admin.site.register(ShareInformation)
