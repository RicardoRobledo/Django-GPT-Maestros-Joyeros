import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from django.conf import settings

from rest_framework import exceptions

from ..serializers.token_serializers import GPTTokenObtainPairSerializer


def decode_token(token:str):
    """
    This function decode a token 

    :param token: a jwt token with user information
    :return: a decoded jwt token
    """

    try:

        return jwt.decode(token, settings.CLIENT_SECRET, algorithms=settings.HASH_ALGORITHM)

    except ExpiredSignatureError:
        raise exceptions.NotAuthenticated(detail='Invalid token')
    except InvalidTokenError:
        raise exceptions.NotAuthenticated(detail='Invalid token')


def create_token(user):
    """
    This function create a token 

    :param user: a user instance
    :return: a jwt token
    """

    tokens = GPTTokenObtainPairSerializer.get_token(user)
    tokens = {
        'token_type':'bearer',
        'access_token':str(tokens.access_token),
        'exp':settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'refresh_token':str(tokens),
        'refresh_expires_in':settings.REFRESH_TOKEN_EXPIRE_SECONDS
    }

    return tokens
