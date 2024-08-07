import random

from maestros_joyeros.customers.models import CustomerModel


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['get_random_customer']


def get_random_customer():
    """
    Select a random customer from the database
    """

    customers = CustomerModel.objects.all()
    return random.choice(customers)
