from django.apps import AppConfig


class CarsharingConfig(AppConfig):
    name = 'carsharing'


def check_card_validality(card_no):
    # request PG to check card's validality
    return True;
