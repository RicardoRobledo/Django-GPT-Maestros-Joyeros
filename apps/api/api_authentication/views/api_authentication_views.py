from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework import status

from apps.users.models import UserModel
from ..utils import token_handlers


@api_view(['POST'])
@permission_classes([AllowAny])
def generate_gpt_tokens(request):
    """
    This view post a message
    """

    form = request.data

    if 'grant_type' not in form:
        raise NotFound(detail='grant_type not found')

    token = None

    if form['grant_type'] == 'authorization_code':
        token = token_handlers.decode_token(form['code'])
    elif form['grant_type'] == 'refresh_token':
        token = token_handlers.decode_token(form['refresh_token'])

    if token is None:
        raise NotFound(detail='Invalid grant type or credentials')

    user = UserModel.objects.filter(username=token['username'])

    if not user.exists():
        raise NotFound(detail='User not found')
    
    token = token_handlers.create_token(user.first())

    return Response(token, status=status.HTTP_200_OK)
