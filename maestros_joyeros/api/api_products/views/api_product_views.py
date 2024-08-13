from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from maestros_joyeros.products.models import ProductModel
from maestros_joyeros.users.utils import user_handlers

from ..serializers.product_serializers import ProductListSerializer, ProductDetailSerializer


__author__ = 'Ricardo'
__version__ = '0.1'


product_list_response = openapi.Response(
    description="Lista de productos existentes",
    examples={
        'application/json': {
            "existing_products": [
                {
                    "product_name": "Producto A",
                },
                {
                    "product_name": "Producto B",
                }
            ]
        }
    }
)


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene los productos existentes",
    operation_id="GetProducts",
    responses={
        status.HTTP_200_OK: product_list_response,
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="No autorizado"),
    },
    tags=['Products']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request):
    """
    This view get our products
    """

    products = ProductModel.objects.all()
    product_serializer = ProductListSerializer(products, many=True)

    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'existing_products': product_serializer.data}, content_type='application/json', status=status.HTTP_200_OK)


product_name_parameter = openapi.Parameter(
    'product_name',
    openapi.IN_PATH,
    description="Nombre del producto",
    type=openapi.TYPE_STRING,
    required=True,
)

product_detail_response = openapi.Response(
    description="Detalles del producto",
    examples={
        'application/json': {
            'product': {
                "product_name": "Producto A",
                "description": "El producto A consiste en ...",
            }
        }
    })


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene un producto específico por nombre",
    operation_id="GetProduct",
    parameters=[
        product_name_parameter
    ],
    responses={
        status.HTTP_200_OK: product_detail_response,
        status.HTTP_404_NOT_FOUND: openapi.Response(description="Producto no encontrado"),
    },
    tags=['Products']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, product_name):
    """
    This view get a product
    """

    product = ProductModel.objects.filter(product_name=product_name)

    if not product.exists():
        user_handlers.register_action(
            request=request, status_code=status.HTTP_404_NOT_FOUND)
        raise NotFound('Product not found', code=status.HTTP_404_NOT_FOUND)

    product_serializer = ProductDetailSerializer(product.first())
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'product': product_serializer.data}, content_type='application/json', status=status.HTTP_200_OK)
