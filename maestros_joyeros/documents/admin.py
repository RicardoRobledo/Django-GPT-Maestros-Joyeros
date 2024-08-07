from django.contrib import admin

from .models import TopicModel, DocumentModel
from .input_filters.document_input import WeightTextInputFilter

from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)


class TopicAdmin(admin.ModelAdmin):

    search_fields = ('topic_name', 'id',)

    list_display = ('id', 'topic_name', 'created_at', 'updated_at',)

    fieldsets = (
        (
            None, {'fields': ('topic_name', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at',)


class DocumentAdmin(admin.ModelAdmin):

    search_fields = ('document_name', 'id',)

    list_filter = (WeightTextInputFilter,
                   'for_workshop',
                   'for_simulation',
                   ('created_at', DateRangeQuickSelectListFilterBuilder()),
                   ('updated_at', DateRangeQuickSelectListFilterBuilder()),)

    list_display = ('id', 'document_name', 'weight',
                    'created_at', 'updated_at',)

    fieldsets = (
        (None, {'fields': ('document_name', 'content', 'weight',
         'for_workshop', 'for_simulation', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(TopicModel, TopicAdmin)
admin.site.register(DocumentModel, DocumentAdmin)
