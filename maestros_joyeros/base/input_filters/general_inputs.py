from django.contrib import messages

from maestros_joyeros.users.models import UserModel
from maestros_joyeros.base.input_filters.base_inputs import TextInputFilter


__author__ = 'Ricardo'
__version__ = '0.1'


class AverageTextInputFilter(TextInputFilter):

    title = 'Average'
    parameter_name = 'average'

    def queryset(self, request, queryset):

        if self.value():

            try:
                average = int(self.value())

                if not (average >= 1 and average <= 10):
                    self.message_user(
                        request, "Average debe ser entre 1 y 10", level=messages.WARNING)
                    return queryset.none()

                averages_gotten = queryset.filter(average=average)

                if averages_gotten.exists():
                    return averages_gotten

                self.message_user(
                    request, "Ninguna registro fue encontrado con ese promedio", level=messages.WARNING)

            except (ValueError, TypeError):
                self.message_user(
                    request, "Average debe ser un número entero", level=messages.ERROR)

            return queryset.none()

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)


class UserUsernameTextInputFilter(TextInputFilter):

    title = 'Username'
    parameter_name = 'username'

    def queryset(self, request, queryset):

        if self.value():

            username = self.value()

            user = UserModel.objects.filter(
                username__icontains=username)

            if user.exists():
                return queryset.filter(user_id=user.first().id)

            self.message_user(
                request, "Ningún usuario fue encontrado con ese nombre de usuario", level=messages.WARNING)

            return queryset.none()

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)


class UserFirstNameTextInputFilter(TextInputFilter):

    title = 'First name'
    parameter_name = 'first_name'

    def queryset(self, request, queryset):

        if self.value():

            first_name = self.value()

            user = UserModel.objects.filter(
                first_name__icontains=first_name)

            if user.exists():
                return queryset.filter(user_id=user.first().id)

            self.message_user(
                request, "Ningún usuario fue encontrado con ese primer nombre", level=messages.WARNING)

            return queryset.none()

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)
