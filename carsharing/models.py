from django.db import models
from django.contrib.auth.models import User


class Lender(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=100)


class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_no = models.CharField(max_length=100)


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
    owner = models.ForeignKey(Lender, on_delete=models.CASCADE)

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
    duration = models.TimeField()


class ShareInformation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    lender = models.ForeignKey(Lender, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, null=True)
    station = models.ForeignKey(SharingStation, on_delete=models.CASCADE)
    fee = models.IntegerField(null=True)
    share_time = models.ForeignKey(ShareTime, on_delete=models.CASCADE)
    status = models.IntegerField()
    # status// 0: registered, 1: reserved, 2: borrowed, 3: returned, 4: lender confirmed
