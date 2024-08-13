from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from django.contrib.auth import logout


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['swagger_logout']


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def swagger_logout(request):

    logout(request)

    return Response(status=204)
