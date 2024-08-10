from datetime import timedelta
from django.utils import timezone


from django.db.models import Sum, Count, F, Q, ExpressionWrapper, FloatField, Prefetch
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from rangefilter.filters import (
    DateRangeQuickSelectListFilterBuilder,
)

import pandas as pd

from .models import UserModel, UserActionModel
from .utils.pdf_managers import create_single_report, create_branch_report

from .input_filters import user_action_inputs
from maestros_joyeros.base.input_filters import general_inputs
from maestros_joyeros.branches.input_filters import branch_inputs

from maestros_joyeros.documents.models import TopicModel
from maestros_joyeros.branches.models import BranchModel
from maestros_joyeros.evaluations.models import SimulationModel, ScoreModel, WorkshopEvaluationModel


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

    list_filter = (branch_inputs.BranchTextInputFilter,
                   ('created_at', DateRangeQuickSelectListFilterBuilder()),
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
                request, "Por favor selecciona solo 1 usuario para generar el reporte.", level=messages.ERROR)
            # return
            return None

        user = queryset[0]

        # day range to filter
        day_range = get_day_range_filter()

        # Getting simulation evaluations

        user_simulations = SimulationModel.objects.filter(
            user_id=user.id,
            created_at__gte=day_range
        )

        total_simulations = user_simulations.count()

        # Doing simulation calculations to get the sum of the scores grouped by metric_id for the filtered simulations

        user_scores = ScoreModel.objects.filter(
            simulation_id__in=user_simulations
        ).values(
            'metric_id'
        ).annotate(
            metric_name=F('metric_id__metric_name'),
            metric_average=ExpressionWrapper(
                Sum('score')/total_simulations, output_field=FloatField())
        )

        # Getting workshop evaluations

        user_workshop_evaluations = WorkshopEvaluationModel.objects.filter(
            user_id=user.id,
            created_at__gte=day_range
        ).select_related(
            'topic_workshop_evaluations'
        ).values(
            'topic_id',
        ).annotate(
            topic_name=F('topic_id__topic_name'),
            topic_count=Count('topic_id'),
            topic_average=ExpressionWrapper(
                Sum('average')/Count('topic_id'), output_field=FloatField())
        )

        # Getting total workshops

        total_workshops = user_workshop_evaluations.aggregate(
            total_workshops=Sum('topic_count'))['total_workshops']

        if total_workshops is None:
            total_workshops = 0

        response = create_single_report(
            user, total_simulations, user_scores, total_workshops, user_workshop_evaluations)

        return response

    @admin.action(description="Generate branch report")
    def generate_branch_report(self, request, queryset):

        # Gettings branches

        branch_name = request.GET.get('branch_name', None)

        if not branch_name:

            self.message_user(
                request, "Debes de filtrar por el nombre de una sucursal", level=messages.ERROR)

            return None

        branch_gotten = BranchModel.objects.filter(
            branch_name__icontains=branch_name)

        if not branch_gotten.exists():

            self.message_user(
                request, "Debes de asegurarte de que la sucursal exista", level=messages.ERROR)

            return None

        # day range to filter

        day_range = get_day_range_filter()

        # Getting users

        users = queryset.exclude(
            Q(is_staff=True) | ~Q(branch_id__branch_name__icontains=branch_name)
        ).filter(
            created_at__gte=day_range
        )

        if users.count() == 0:

            self.message_user(
                request, "Debes de elegir un usuario o más y no deben de ser personal", level=messages.ERROR)

            return None

        # Getting simulation identifiers

        simulation_ids = []

        user_branch_simulations = users.prefetch_related(
            Prefetch('user_simulations',
                     queryset=SimulationModel.objects.filter(created_at__gte=day_range).only('id'))
        )

        for user in user_branch_simulations:

            user_simulation_ids = list(
                user.user_simulations.values_list('id', flat=True))

            simulation_ids.extend(user_simulation_ids)

        # Getting simulations and scores

        simulation_scores_gotten = []

        simulations = SimulationModel.objects.filter(id__in=simulation_ids)

        simulation_related_scores = simulations.prefetch_related(
            Prefetch('simulation_scores',
                     queryset=ScoreModel.objects.filter(created_at__gte=day_range).only('id'))
        )

        for simulation_scores in simulation_related_scores:

            user_simulation_scores = list(
                simulation_scores.simulation_scores.all().values(
                    'metric_id__metric_name', 'score'
                ).annotate(
                    metric_name=F('metric_id__metric_name')
                ).values(
                    'metric_name', 'score'
                ))

            simulation_scores_gotten.extend(user_simulation_scores)

        # Doing simulation calculations for the report

        df = pd.DataFrame(simulation_scores_gotten)

        total_simulations = simulations.count()
        user_simulation_scores = []

        if not total_simulations == 0:

            grouped_df = df.groupby('metric_name').agg(
                metric_average=('score', 'mean')
            ).reset_index()

            grouped_df['metric_average'] = grouped_df['metric_average'].round(
                1)
            simulation_scores = grouped_df.to_dict(orient='records')

            user_simulation_scores.extend(simulation_scores)

        # Getting workshop evaluations

        user_workshop_evaluations = WorkshopEvaluationModel.objects.filter(
            user_id__in=[user.id for user in users],
            created_at__gte=day_range
        ).select_related(
            'topic_workshop_evaluations'
        ).values(
            'topic_id',
        ).annotate(
            topic_name=F('topic_id__topic_name'),
            topic_count=Count('topic_id'),
            topic_average=ExpressionWrapper(
                Sum('average')/Count('topic_id'), output_field=FloatField())
        )

        total_workshops = user_workshop_evaluations.aggregate(
            topic_sum=Sum('topic_count'))['topic_sum']

        if total_workshops is None:
            total_workshops = 0

        response = create_branch_report(
            branch_name.replace(' ', '_'), total_simulations, user_simulation_scores, total_workshops, user_workshop_evaluations)

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
                   user_action_inputs.UserActionMethodTextInputFilter,
                   user_action_inputs.UserActionStatusCodeTextInputFilter,
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
