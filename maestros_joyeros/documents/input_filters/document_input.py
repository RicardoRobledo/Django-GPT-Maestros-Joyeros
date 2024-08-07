from django.contrib import messages

from maestros_joyeros.base.input_filters.base_inputs import TextInputFilter


__author__ = 'Ricardo'
__version__ = '0.1'


class WeightTextInputFilter(TextInputFilter):

    title = 'Weight'
    parameter_name = 'weight'

    def queryset(self, request, queryset):

        if self.value():

            try:

                weight = int(self.value())

                if not (weight >= 1 and weight <= 10):

                    self.message_user(
                        request, "Weight debe ser entre 1 y 10", level=messages.WARNING)
                    return queryset.none()

                weights_gotten = queryset.filter(weight=weight)

                if weights_gotten.exists():
                    return weights_gotten

                self.message_user(
                    request, "Ningun score fue encontrado con ese puntaje", level=messages.WARNING)

                return queryset.filter(weight=weight)

            except (ValueError, TypeError):
                self.message_user(
                    request, "Weight debe ser un número entero", level=messages.ERROR)

            return queryset.none()

        return queryset

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)
