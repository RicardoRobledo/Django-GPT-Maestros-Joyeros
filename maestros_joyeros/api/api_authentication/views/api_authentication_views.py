from django.conf import settings
from django.contrib.auth import logout

from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from maestros_joyeros.users.models import UserModel
from ..utils import token_handlers


__author__ = 'Ricardo'
__version__ = '1.0'


@swagger_auto_schema(method='post', auto_schema=None)
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_gpt_tokens(request):
    """
    This view post a message
    """

    form = request.data

    if not all(valor in form for valor in ('grant_type', 'client_secret', 'client_id')):
        raise ParseError(
            detail='grant_type, client_secret or client_id not found')

    if not form['client_secret'] == settings.CLIENT_SECRET and not form['client_id'] == settings.CLIENT_ID:
        raise AuthenticationFailed(
            detail='client_secret or client_id are incorrect')

    token = None

    if form['grant_type'] == 'authorization_code':
        token = token_handlers.decode_token(form['code'])
    elif form['grant_type'] == 'refresh_token':
        token = token_handlers.decode_token(form['refresh_token'])

    if token is None:
        raise ParseError(detail='Invalid grant type or credentials')

    user = UserModel.objects.filter(username=token['username'])

    if not user.exists():
        raise AuthenticationFailed(detail='User not found')

    token = token_handlers.create_token(user.first())

    return Response(token, content_type='application/json', status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def swagger_logout(request):

    logout(request)

    return Response(status=204)
