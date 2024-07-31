from django.contrib import admin

from .models import ProductModel


class ProductAdmin(admin.ModelAdmin):

    search_fields = ('id', 'product_name',) 
    
    list_display = ('id', 'product_name', 'created_at', 'updated_at',)
    
    fieldsets = (
    (
        None, {'fields': ('product_name', 'description', 'weight', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(ProductModel, ProductAdmin)
