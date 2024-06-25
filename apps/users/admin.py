from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserModel, UserActionModel, WeakPointModel, StrongPointModel


class UserAdmin(BaseUserAdmin):
    
    list_display = ('username', 'id', 'created_at', 'updated_at', 'is_active', 'is_staff', 'is_superuser')
    
    fieldsets = (
    (
        None, {'fields': ('username', 'middle_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')}),
    )

    readonly_fields = ('created_at', 'updated_at')


admin.site.register(UserModel, UserAdmin)
admin.site.register(UserActionModel)
admin.site.register(WeakPointModel)
admin.site.register(StrongPointModel)
