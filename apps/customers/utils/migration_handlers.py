import os
from apps.base.utils.file_handlers import read_customer_files


__author__ = 'Ricardo'
__version__ = '1.0'


def insert_customer_data(apps, schema_editor):

    CustomerModel = apps.get_model('customers', 'CustomerModel')

    customers = read_customer_files('Información/Clientes')
    CustomerModel.objects.bulk_create(customers)
