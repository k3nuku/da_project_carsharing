from django.db import models
from geoposition.fields import GeopositionField


class CarDescription(models.Model):
    color = models.CharField(max_length=10)
    submodel = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='images/car', blank=True)

    def __str__(self):
        return self.submodel + ', ' + self.color


class Car(models.Model):
    model = models.CharField(max_length=100)
    grade = models.IntegerField()
    license_plate = models.CharField(max_length=100)
    description = models.OneToOneField(CarDescription, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}, {2}, [{3}], Color: {4}' \
            .format(self.model, self.description.submodel, self.grade, self.license_plate,
                    self.description.color)


class CarCatalog(models.Model):
    cars = models.ForeignKey(Car, on_delete=models.DO_NOTHING)


class SharingStation(models.Model):
    name = models.CharField(max_length=100)
    location = GeopositionField()
    catalog = models.ForeignKey(CarCatalog, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShareHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    station = models.ForeignKey(SharingStation, on_delete=models.DO_NOTHING)
    fee = models.DecimalField(decimal_places=10, max_digits=10)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
