from django.contrib import admin

from .models import TopicModel, DocumentModel


class TopicAdmin(admin.ModelAdmin):

    search_fields = ('product_name', 'id',) 

    list_display = ('topic_name', 'id', 'created_at', 'updated_at',)
    
    fieldsets = (
    (
        None, {'fields': ('topic_name', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at',)


class DocumentAdmin(admin.ModelAdmin):

    search_fields = ('product_name', 'id',)

    list_filter = ('for_workshop',)
    
    list_display = ('document_name', 'id', 'created_at', 'updated_at',)
    
    fieldsets = (
    (
        None, {'fields': ('document_name', 'content', 'weight', 'for_workshop', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(TopicModel, TopicAdmin)
admin.site.register(DocumentModel, DocumentAdmin)
