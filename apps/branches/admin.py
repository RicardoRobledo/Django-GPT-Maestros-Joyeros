from django.contrib import admin

from .models import BranchModel


class BranchAdmin(admin.ModelAdmin):

    list_display = ('id', 'branch_name', 'state', 'created_at', 'updated_at')


admin.site.register(BranchModel, BranchAdmin)
