from django.contrib import admin

from .models import ProductModel


class ProductAdmin(admin.ModelAdmin):

    search_fields = ('product_name', 'id',) 
    
    list_display = ('product_name', 'id', 'created_at', 'updated_at',)
    
    fieldsets = (
    (
        None, {'fields': ('product_name', 'description', 'weight', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(ProductModel, ProductAdmin)
