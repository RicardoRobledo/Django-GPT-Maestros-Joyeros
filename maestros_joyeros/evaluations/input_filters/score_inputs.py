from django.contrib import messages

from maestros_joyeros.base.input_filters.base_inputs import TextInputFilter
from maestros_joyeros.users.models import UserModel


__author__ = 'Ricardo'
__version__ = '0.1'


class ScoreTextInputFilter(TextInputFilter):

    title = 'Score'
    parameter_name = 'score'

    def queryset(self, request, queryset):

        if self.value():
            try:
                score = int(self.value())

                if not (score >= 1 and score <= 10):
                    self.message_user(
                        request, "Score debe ser entre 1 y 10", level=messages.WARNING)
                    return queryset.none()

                scores_gotten = queryset.filter(score=score)

                if scores_gotten.exists():
                    return scores_gotten

                self.message_user(
                    request, "Ningun score fue encontrado con ese puntaje", level=messages.WARNING)

            except (ValueError, TypeError):
                self.message_user(
                    request, "Score debe ser un número entero", level=messages.ERROR)

            # return queryset
            return queryset.none()

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)


class ScoreUserTextInputFilter(TextInputFilter):

    title = 'Username'
    parameter_name = 'username'

    def queryset(self, request, queryset):

        if self.value():

            username = self.value()

            user = UserModel.objects.filter(
                username__icontains=username)

            if user.exists():
                return queryset.filter(simulation_id__user_id=user.first().id)

            self.message_user(
                request, "Ningún usuario fue encontrado con ese nombre de usuario", level=messages.WARNING)

            return queryset

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)


class ScoreUserFirstNameTextInputFilter(TextInputFilter):

    title = 'First name'
    parameter_name = 'first_name'

    def queryset(self, request, queryset):

        if self.value():

            first_name = self.value()

            user = UserModel.objects.filter(
                first_name__icontains=first_name)

            if user.exists():
                return queryset.filter(simulation_id__user_id=user.first().id)

            self.message_user(
                request, "Ningún usuario fue encontrado con ese primer nombre", level=messages.WARNING)

            return queryset

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)
