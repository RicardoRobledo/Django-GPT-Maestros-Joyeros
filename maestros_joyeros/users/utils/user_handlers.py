from ..models import UserActionModel


__author__ = 'Ricardo'
__version__ = '0.1'


def register_action(request, status_code:int):
    """
    This method is used to register a user action in the database.

    :param request: request object
    :param status_code: status code of the request
    """

    user = request.user

    UserActionModel.objects.create(
        method=request.method,
        path=request.path,
        status_code=status_code,
        user_id=user
    )
