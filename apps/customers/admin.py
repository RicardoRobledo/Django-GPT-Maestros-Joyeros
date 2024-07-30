from django.contrib import admin

from .models import CustomerModel


class CustomerAdmin(admin.ModelAdmin):

    list_display = ('id', 'customer_type', 'created_at', 'updated_at')

    search_fields = ('id', 'customer_type',)


admin.site.register(CustomerModel, CustomerAdmin)
