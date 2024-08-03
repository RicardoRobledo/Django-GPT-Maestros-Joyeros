from datetime import datetime, timedelta

from django.db.models import Sum, Count, F, ExpressionWrapper, FloatField
from django.utils import timezone
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from .models import UserModel, UserActionModel

from .input_filters import user_action_inputs
from apps.base.input_filters import general_inputs

from apps.documents.models import TopicModel
from apps.evaluations.models import SimulationModel, ScoreModel, WorkshopEvaluationModel

from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)

import io
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image, SimpleDocTemplate
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def get_day_range_filter():
    """
    This function returns the date range filter

    :return: day range to filter
    """

    now = timezone.now()
    thirty_days_ago = now - timedelta(days=31)

    return thirty_days_ago


class UserAdmin(BaseUserAdmin):

    list_display = ('id', 'username', 'first_name', 'middle_name',
                    'last_name', 'branch_id', 'created_at', 'updated_at',
                    'is_active', 'is_staff', 'is_superuser')

    list_filter = (('created_at', DateRangeQuickSelectListFilterBuilder()),
                   ('updated_at', DateRangeQuickSelectListFilterBuilder()),)

    search_fields = ('id', 'username', 'first_name', 'middle_name',
                     'last_name', 'email', 'branch_id__branch_name')

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('username', 'first_name', 'middle_name', 'last_name', 'password1', 'password2', 'email', 'branch_id', 'groups', 'is_active', 'is_staff', 'is_superuser',)
            }
        ),
    )

    fieldsets = (
        (
            None, {
                'fields': ('username', 'first_name', 'middle_name', 'last_name', 'password', 'email', 'branch_id', 'groups', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
            }
        ),
    )

    readonly_fields = ('created_at', 'updated_at')

    actions = ['generate_single_report', 'generate_branch_report']

    @admin.action(description="Generate single report")
    def generate_single_report(self, request, queryset):

        if queryset.count() > 1:
            self.message_user(
                request, "Please select only one user to generate the report.", level=messages.ERROR)
            # return
            return None

        user = queryset[0]

        user_simulations = SimulationModel.objects.filter(
            user_id=user.id,
            created_at__gte=get_day_range_filter()
        )

        total_simulations = user_simulations.count()

        # Get the sum of the scores grouped by metric_id for the filtered simulations
        user_scores = ScoreModel.objects.filter(
            simulation_id__in=user_simulations
        ).values(
            'metric_id'
        ).annotate(
            metric_name=F('metric_id__metric_name'),
            metric_average=ExpressionWrapper(
                Sum('score')/total_simulations, output_field=FloatField())
        )

        user_workshop_scores = WorkshopEvaluationModel.objects.filter(
            user_id=user.id,
            created_at__gte=get_day_range_filter()
        ).select_related(
            'topics'
        ).values(
            'topic_id',
        ).annotate(
            topic_name=F('topic_id__topic_name'),
            topic_count=Count('topic_id'),
            topic_average=ExpressionWrapper(
                Sum('average')/Count('topic_id'), output_field=FloatField())
        )

        total_workshops = user_workshop_scores.aggregate(
            total_workshops=Sum('topic_count'))['total_workshops']

        if total_workshops is None:
            total_workshops = 0

        response = self.create_report(
            user, total_simulations, user_scores, total_workshops, user_workshop_scores)

        return response

    @admin.action(description="Generate branch report")
    def generate_branch_report(self, request, queryset):

        user = queryset[0]

        print(request.GET.get('branch_name'))

        return True

    def create_report(self, user, total_simulations, user_scores, total_workshops, user_workshop_scores):

        import matplotlib
        matplotlib.use('Agg')

        def create_radar_chart(metrics, total_simulations):
            # Extraer nombres de las métricas y sus valores
            valores = [metric['metric_average'] for metric in metrics]

            categorias = [
                f"{metric['metric_name']}\n{metric['metric_average']}" for metric in metrics]
            # Asegurarse de que los valores sean un círculo completo
            angulos = np.linspace(
                0, 2 * np.pi, len(categorias), endpoint=False).tolist()
            valores = np.concatenate((valores, [valores[0]]))
            angulos += angulos[:1]

            # Crear el gráfico de radar
            fig, ax = plt.subplots(
                figsize=(14, 14), subplot_kw=dict(polar=True))
            # Verde esmeralda con más transparencia
            ax.fill(angulos, valores, color='#23F4C4', alpha=0.2)
            # Verde oscuro para el borde
            ax.plot(angulos, valores, color='#26CFA8', linewidth=2)

            # Ajustes de las categorías
            # Mostrar ticks del 1 al 10
            ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            ax.set_yticklabels([])
            ax.tick_params(axis='both', which='major', pad=145)
            ax.set_xticks(angulos[:-1])
            ax.set_xticklabels(categorias, fontsize=40, color='#000000')

            # Mejora en el estilo
            # Líneas de cuadrícula en verde claro
            ax.grid(color='#B6B6B6', linestyle='solid')
            ax.set_facecolor('#444444')  # Fondo en un tono verde muy claro

            # Guardar el gráfico en un búfer en memoria
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)

            # Cerrar la figura
            plt.close(fig)

            return buf

        date = timezone.now().strftime('%d-%m-%Y')

        # Create a HttpResponse object with the correct PDF headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f"attachment; filename=Reporte_{user.middle_name}{user.last_name}{user.first_name}_{date}.pdf;"

        # Create the PDF object using reportlab
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        normal_style = styles['Normal']
        heading_style = ParagraphStyle(
            name='Heading', parent=styles['Heading1'], alignment=1, spaceAfter=14, fontSize=16)
        right_aligned_style = ParagraphStyle(
            name='RightAligned', parent=styles['Normal'], alignment=2, spaceAfter=14)

        info = [
            ['Evaluación para vendedores de los últimos 31 días', ''],
            ['Nombre completo',
                f'{user.first_name} {user.middle_name} {user.last_name}'],
            ['Fecha de expedición del reporte', f'{date}']
        ]

        # Añadir columnas de padding
        info_table = Table(info, colWidths=[240, 240])
        info_table.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),  # Span the title across the inner columns
            # Center all cells horizontally
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # Center the title cell vertically
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            # Larger font size for the title
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            # Background color for the title
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            # Text color for the title
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            # Top padding for the title row
            ('TOPPADDING', (0, 0), (-1, -1), 12),  # Top padding for all rows
            # Bottom padding for all rows
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            # Background color for other rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            # Text color for other rows
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 12),  # Font size for other rows
            ('LEFTPADDING', (0, 0), (-1, -1), 12),  # Left padding for all rows
            # Right padding for all rows
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around the table
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))  # Additional spacer after the table

        # Add data table
        data = [["Tema", "Veces que se tomó", "Promedio"]]  # Header
        for metric in user_workshop_scores:
            data.append(
                [metric['topic_name'], metric['topic_count'], metric['topic_average']])

        # Create radar chart and get it as a buffer
        if total_simulations == 0:
            # Subtítulo
            subtitle = Paragraph(
                "El vendedor no ha tomado simulaciones", heading_style)
            elements.append(subtitle)
        else:
            radar_chart_buffer = create_radar_chart(
                user_scores, total_simulations)

            # Subtítulo
            subtitle = Paragraph(
                f"Estadísticas de simulaciones ({total_simulations} hechos)", heading_style)
            elements.append(subtitle)

            # Insert radar chart image into the PDF
            radar_chart_img = Image(radar_chart_buffer)
            radar_chart_img.drawHeight = 3 * inch
            radar_chart_img.drawWidth = 3 * inch

            elements.append(radar_chart_img)
            elements.append(Spacer(1, 36))

        if total_workshops == 0:
            # Subtítulo
            subtitle = Paragraph(
                f"El vendedor no ha tomado talleres", heading_style)
            elements.append(subtitle)
        else:
            subtitle = Paragraph(
                f"Estadísticas de talleres ({total_workshops} hechos)", heading_style)
            elements.append(subtitle)

            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.black),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)

        # intro_text = Paragraph(
        #    f"<strong>Número de simulaciones hechas:</strong> {total_simulations}.",
        #    normal_style
        # )
        # elements.append(intro_text)

        elements.append(Spacer(1, 60))

        # Build PDF
        doc.build(elements)

        return response

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        # if is superuser show all users
        if request.user.is_superuser:
            # self.list_filter = self.list_filter.append(branch_inputs.BranchInputFilter)
            return qs

        return qs.filter(branch_id=request.user.branch_id)


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
