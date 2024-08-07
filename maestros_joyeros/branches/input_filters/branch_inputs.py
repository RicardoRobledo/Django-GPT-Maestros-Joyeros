from django.contrib import messages

from maestros_joyeros.base.input_filters.base_inputs import TextInputFilter


__author__ = 'Ricardo'
__version__ = '0.1'


class BranchTextInputFilter(TextInputFilter):

    title = 'Branch'
    parameter_name = 'branch_name'

    def queryset(self, request, queryset):

        if self.value():

            branch_name = self.value()

            branches = queryset.filter(
                branch_id__branch_name__icontains=branch_name)

            if branches.exists():
                return branches

            self.message_user(
                request, "Ninguna sucursal fue encontrada con ese nombre", level=messages.WARNING)

        return queryset

    def message_user(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)
