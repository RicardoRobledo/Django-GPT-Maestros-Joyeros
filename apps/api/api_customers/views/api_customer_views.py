from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view

from apps.users.models import UserModel
from apps.customers.models import CustomerModel

from apps.users.utils import user_handlers


__author__ = 'Ricardo'
__version__ = '0.1'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customers(request):
    """
    This view return us a the client types we have
    """

    customer_types = CustomerModel.objects.all().values_list('customer_type', flat=True)
    user_handlers.register_action(request=request, status_code=status.HTTP_200_OK)

    return Response({'customer_types':customer_types}, content_type='application/json', status=status.HTTP_200_OK)

