from django.contrib import admin

from .models import TopicModel, DocumentModel


class TopicAdmin(admin.ModelAdmin):

    search_fields = ('topic_name', 'id',) 

    list_display = ('topic_name', 'id', 'created_at', 'updated_at',)
    
    fieldsets = (
    (
        None, {'fields': ('topic_name', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at',)



class TextInputFilter(admin.SimpleListFilter):
    template = 'documents/input_filter.html'  # Ruta al template personalizado

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.

        for k, v in changelist.get_filters_params().items():
            if k != self.parameter_name:
                print(f'k: {k}, v: {v} -> {self.parameter_name}')

        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v if not isinstance(v, list) else v[0])
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class WeightTextInputFilter(TextInputFilter):
    title = 'Weight'
    parameter_name = 'weight'

    def queryset(self, request, queryset):

        if self.value():
            try:
                weight = int(self.value())
                print(f"Applying weight filter: {weight}")
                print(f"Current filters: {request.GET}")
                return queryset.filter(weight=weight)
            except (ValueError, TypeError):
                return queryset.none()
        return queryset


class DocumentAdmin(admin.ModelAdmin):

    search_fields = ('document_name', 'id',)

    list_filter = (WeightTextInputFilter, 'for_workshop', 'for_simulation',)
    
    list_display = ('document_name', 'id', 'created_at', 'updated_at',)
    
    fieldsets = (
        (None, {'fields': ('document_name', 'content', 'weight', 'for_workshop', 'for_simulation', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(TopicModel, TopicAdmin)
admin.site.register(DocumentModel, DocumentAdmin)
