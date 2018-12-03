from django.db import models
from colorfield.fields import ColorField
from geoposition.fields import GeopositionField

class Car(models.Model, CarDescription):
  model = models.CharField(max_length=100)
  grade = models.DecimalField(max_digits=1)
  license_plate = models.CharField(max_length=100)
  description = models.ForeignKey(
    CarDescription, on_delete=models.CASCADE)

class CarDescription(models.Model):
  color = ColorField(default='#000000')
  submodel = models.CharField(max_length=50)

class SharingStation(models.Model):
  name = models.CharField(max_length=100)
  location = GeopositionField()
