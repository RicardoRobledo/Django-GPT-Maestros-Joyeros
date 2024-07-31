from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest, HttpResponse

from .models import UserModel, UserActionModel

from apps.evaluations.models import SimulationModel

from .input_filters import user_action_inputs
from apps.base.input_filters import general_inputs

from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)


class UserAdmin(BaseUserAdmin):

    list_display = ('id', 'username', 'first_name', 'middle_name',
                    'last_name',  'created_at', 'updated_at',
                    'is_active', 'is_staff', 'is_superuser')

    list_filter = (('created_at', DateRangeQuickSelectListFilterBuilder()),
                   ('updated_at', DateRangeQuickSelectListFilterBuilder()),)

    search_fields = ('id', 'username', 'first_name',
                     'middle_name', 'last_name', 'email',)

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('username', 'first_name', 'middle_name', 'last_name', 'password1', 'password2', 'email', 'groups', 'is_active', 'is_staff', 'is_superuser',)
            }
        ),
    )

    fieldsets = (
        (
            None, {
                'fields': ('username', 'first_name', 'middle_name', 'last_name', 'password', 'email', 'groups', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
            }
        ),
    )

    readonly_fields = ('created_at', 'updated_at')

    actions = ['crear_reporte']

    @admin.action(description="Create report")
    def crear_reporte(modeladmin, request, queryset):

        user = queryset[0]

        now = timezone.now()
        thirty_days_ago = now - timedelta(days=31)

        print(SimulationModel.objects.filter(
            user_id=user.id, created_at__gte=thirty_days_ago))
        print()
        print()
        '''from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        # Crear un objeto HttpResponse con las cabeceras PDF correctas.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

        # Crear el objeto PDF utilizando reportlab.
        p = canvas.Canvas(response, pagesize=letter)
        p.setFont("Helvetica", 12)

        # Escribir en el PDF. Puedes personalizar esto según tus necesidades.
        p.drawString(100, 750, "Reporte de ejemplo")
        p.drawString(100, 730, "Lista de elementos seleccionados:")

        y = 710
        for obj in queryset:
            p.drawString(100, y, str(obj))
            y -= 20

        # Terminar el PDF.
        p.showPage()
        p.save()'''

        return True


class UserActionAdmin(admin.ModelAdmin):

    save_as = False
    save_as_continue = False
    delete_confirmation_template = False

    list_display = ('id', 'user_id', 'method', 'status_code',
                    'created_at', 'updated_at')

    list_filter = (general_inputs.UserTextInputFilter,
                   user_action_inputs.UserActionMethodInputFilter,
                   user_action_inputs.UserActionStatusCodeInputFilter,
                   ('created_at', DateRangeQuickSelectListFilterBuilder()),)

    fieldsets = (
        (
            None, {'fields': ('user_id', 'method', 'path',
                              'status_code', 'created_at', 'updated_at',)}
        ),
    )

    search_fields = ('id',)

    readonly_fields = ('id',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super(UserActionAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(UserModel, UserAdmin)
admin.site.register(UserActionModel, UserActionAdmin)
