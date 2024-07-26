from django.contrib import admin

from .models import BranchModel


class BranchAdmin(admin.ModelAdmin):

    list_display = ('branch_name', 'id', 'state', 'created_at', 'updated_at')


admin.site.register(BranchModel, BranchAdmin)
