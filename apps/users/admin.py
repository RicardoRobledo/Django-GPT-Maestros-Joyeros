from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest

from .models import UserModel, UserActionModel


from django.http import HttpResponse
class UserAdmin(BaseUserAdmin):

    list_display = ('username', 'id', 'created_at', 'updated_at', 'is_active', 'is_staff', 'is_superuser')

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
    @admin.action(description="Mark selected stories as published")
    def crear_reporte(modeladmin, request, queryset):
        from reportlab.lib.pagesizes import letter
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
        p.save()

        return response


class UserActionAdmin(admin.ModelAdmin):
    
    save_as = False
    save_as_continue = False
    delete_confirmation_template = False

    list_display = ('id', 'method', 'status_code', 'created_at', 'updated_at')

    fieldsets = (
    (
        None, {'fields': ('user_id', 'method', 'path', 'status_code', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('user_id', 'method', 'path', 'status_code', 'created_at', 'updated_at')

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
