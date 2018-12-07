from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime

from carsharing import models

class register_car_unit_test(TestCase):
    def insert(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='1234'
        )
