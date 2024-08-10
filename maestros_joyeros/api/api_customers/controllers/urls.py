from django.urls import path

from ..views import api_customer_views


__author__ = 'Ricardo'
__version__ = '0.1'


app_name = 'api_customers'


urlpatterns = [
    path('', api_customer_views.get_customers, name='get_customers'),
]
