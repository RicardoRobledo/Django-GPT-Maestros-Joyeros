from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from maestros_joyeros.products.models import ProductModel
from maestros_joyeros.users.utils import user_handlers

from ..serializers.product_serializers import ProductListSerializer, ProductDetailSerializer


__author__ = 'Ricardo'
__version__ = '0.1'


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
