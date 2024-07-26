from django.urls import path

from ..views import api_customer_views


__author__ = 'Ricardo'
__version__ = '0.1'


urlpatterns = [
    path('', api_customer_views.get_customers),
]
