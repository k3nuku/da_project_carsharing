from django.db import models
from geoposition.fields import GeopositionField


class CarDescription(models.Model):
    color = models.CharField(max_length=10)
    submodel = models.CharField(max_length=50)


class Car(models.Model):
    model = models.CharField(max_length=100)
    grade = models.DecimalField(decimal_places=0, max_digits=3)
    license_plate = models.CharField(max_length=100)
    description = models.ForeignKey(CarDescription, on_delete=models.CASCADE)


class CarCatalog(models.Model):
    cars = models.ForeignKey(Car, on_delete=models.DO_NOTHING)


class SharingStation(models.Model):
    name = models.CharField(max_length=100)
    location = GeopositionField()
    catalog = models.ForeignKey(CarCatalog, on_delete=models.CASCADE)


class ShareHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    station = models.ForeignKey(SharingStation, on_delete=models.DO_NOTHING)
    fee = models.DecimalField(decimal_places=10, max_digits=10)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
