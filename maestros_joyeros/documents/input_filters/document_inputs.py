from django.contrib import messages

from maestros_joyeros.base.input_filters.base_inputs import TextInputFilter
from ..models import TopicModel


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


class TopicNameTextInputFilter(TextInputFilter):

    title = 'Topic Name'
    parameter_name = 'topic_name'

    def queryset(self, request, queryset):

        if self.value():

            topic_name = self.value()

            topic_gotten = TopicModel.objects.filter(
                topic_name__icontains=topic_name)

            if not topic_gotten.exists():

                self.message_user(
                    request, "Ningun topic fue encontrado con ese nombre", level=messages.WARNING)

                return queryset.none()

            return queryset.filter(topic_id=topic_gotten.first().id)

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)
