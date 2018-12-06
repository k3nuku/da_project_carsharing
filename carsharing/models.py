from django.db import models
from django.contrib.auth.models import User


class CarDescription(models.Model):
    color = models.CharField(max_length=10)
    sub_model = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='images/car', blank=True)

    def __str__(self):
        return self.sub_model + ', ' + self.color


class Car(models.Model):
    model = models.CharField(max_length=100)
    grade = models.IntegerField()
    license_plate = models.CharField(max_length=100)
    description = models.OneToOneField(CarDescription, on_delete=models.CASCADE)

    # for sharing environment
    available = models.BooleanField(default=True)

    def __str__(self):
        return '{0} - {1}, {2}, [{3}], Color: {4}' \
            .format(self.model, self.description.sub_model, self.grade, self.license_plate,
                    self.description.color)


class CarCatalog(models.Model):
    cars = models.ManyToManyField(Car, blank=True)


class SharingStation(models.Model):
    name = models.CharField(max_length=100)
    #location = GeopositionField()
    catalog = models.OneToOneField(CarCatalog, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShareTime(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Lender(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=100)


class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_no = models.CharField(max_length=100)


class ShareInformation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    lender = models.ForeignKey(Lender, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    station = models.ForeignKey(SharingStation, on_delete=models.CASCADE)
    fee = models.DecimalField(decimal_places=10, max_digits=10)
    share_time = models.ForeignKey(ShareTime, on_delete=models.CASCADE)
    status = models.IntegerField()
    # status// 0: reserved, 1: borrowed, 2: returned, 3: lender confirmed
