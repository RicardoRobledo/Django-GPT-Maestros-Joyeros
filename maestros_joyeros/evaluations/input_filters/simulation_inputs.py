from django.contrib import messages

from maestros_joyeros.base.input_filters.base_inputs import TextInputFilter


__author__ = 'Ricardo'
__version__ = '0.1'


class SimulationTextInputFilter(TextInputFilter):

    title = 'Simulation'
    parameter_name = 'simulation'

    def queryset(self, request, queryset):

        if self.value():

            try:

                simulation_id = int(self.value())
                simulations_gotten = queryset.filter(
                    simulation_id=simulation_id)

                if simulations_gotten.exists():
                    return simulations_gotten

                self.message_user(
                    request, "Ninguna simulación fue encontrada con ese id", level=messages.WARNING)

            except (ValueError, TypeError):
                self.message_user(
                    request, "Simulation id debe ser un número entero", level=messages.ERROR)

            return queryset.none()

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)
