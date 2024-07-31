from enum import Enum

from django.contrib import messages

from apps.base.input_filters.base_inputs import TextInputFilter


__author__ = 'Ricardo'
__version__ = '0.1'
__all__ = ['UserActionInputFilter']


class HttpMethodEnum(Enum):

    POST = 'POST'
    GET = 'GET'

    @classmethod
    def is_valid_method(cls, value):
        return value in cls._value2member_map_


class UserActionMethodInputFilter(TextInputFilter):

    title = 'Method'
    parameter_name = 'method'

    def queryset(self, request, queryset):

        if self.value():

            method = self.value()

            if not HttpMethodEnum.is_valid_method(method):

                self.message_user(
                    request, "El valor no es un método válido", level=messages.WARNING)
                return queryset.none()

            else:

                return queryset.filter(method=method)

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)


class UserActionStatusCodeInputFilter(TextInputFilter):

    title = 'Status code'
    parameter_name = 'status_code'

    def queryset(self, request, queryset):

        if self.value():

            try:

                status_code = int(self.value())

                if not self.is_valid_http_status_code(status_code):

                    self.message_user(
                        request, "El código de estatus no es válido", level=messages.WARNING)

                else:
                    return queryset.filter(status_code=status_code)

            except (ValueError, TypeError):

                self.message_user(
                    request, "Status code debe ser un numero entero", level=messages.ERROR)

            return queryset.none()

    def is_valid_http_status_code(self, code):
        """
        Verifify if the code is a valid http status code

        :params code: http status code
        :returns: a boolean indicating if the code is valid
        """

        valid_ranges = [
            (100, 103),  # 1xx Informational
            (200, 226),  # 2xx Success
            (300, 308),  # 3xx Redirection
            (400, 451),  # 4xx Client Error
            (500, 511)   # 5xx Server Error
        ]

        return any(start <= code <= end for start, end in valid_ranges)

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)
