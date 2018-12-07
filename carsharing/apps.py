from django.apps import AppConfig
from carsharing import models


class CarsharingConfig(AppConfig):
    name = 'carsharing'


def check_card_validality(card_no):
    # request PG to check card's validality
    return True;


def lender(user):
    try:
        models.Lender.objects.get(user=user)
        return True
    except:
        return False


def borrower(user):
    try:
        models.Borrower.objects.get(user=user)
        return True
    except:
        return False
