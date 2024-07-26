import random

from apps.customers.models import CustomerModel


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['get_random_customer', 'get_customer']


def get_random_customer():
    """
    Select a random customer from the database
    """

    customers = CustomerModel.objects.all()
    return random.choice(customers)


def get_customer(profile):
    """
    Select a customer from the database

    :param profile: str being the profile of the customer
    """

    customer = CustomerModel.objects.filter(customer_type=profile)
    return customer.first()
