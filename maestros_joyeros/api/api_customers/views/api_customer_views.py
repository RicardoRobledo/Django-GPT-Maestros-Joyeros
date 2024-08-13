from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from maestros_joyeros.customers.models import CustomerModel
from maestros_joyeros.users.utils import user_handlers


__author__ = 'Ricardo'
__version__ = '0.1'


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene los tipos de clientes existentes",
    operation_id="GetCustomers",
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Lista de tipos de clientes",
            examples={
                "application/json": {
                    "customer_types": [
                        "Deportista",
                        "Artista",
                        "Actor"
                    ]
                }
            }
        ),
    },
    tags=['Customers']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customers(request):
    """
    This view return us a the client types we have
    """

    customer_types = CustomerModel.objects.all().values_list('customer_type', flat=True)
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'customer_types': customer_types}, content_type='application/json', status=status.HTTP_200_OK)
