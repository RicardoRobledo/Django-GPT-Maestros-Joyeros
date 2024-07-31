from django.contrib import admin


__author__ = 'Ricardo'
__version__ = '0.1'


class TextInputFilter(admin.SimpleListFilter):

    # Path to custom template
    template = 'base/input_filter.html'

    # def lookups(self, request, model_admin):
    #    return ((None, None),)

    def choices(self, changelist):

        all_choice = next(super().choices(changelist))

        all_choice['query_parts'] = (
            (k, v if not isinstance(v, list) else v[0])
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )

        yield all_choice
