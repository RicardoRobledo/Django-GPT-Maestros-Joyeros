from django.contrib import admin

from ..base.input_filters import general_inputs
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)

from .models import MetricModel, ScoreModel, SimulationModel, WorkshopEvaluationModel

from .input_filters import (
    score_inputs,
    simulation_inputs
)


class SimulationAdmin(admin.ModelAdmin):

    list_display = ('id', 'get_username', 'average',
                    'created_at', 'updated_at')

    list_filter = (general_inputs.AverageTextInputFilter,
                   general_inputs.UserTextInputFilter,
                   ("created_at", DateRangeQuickSelectListFilterBuilder()),)

    # search_fields = ('id', 'user_id__username')
    search_fields = ('id',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def get_username(self, obj):
        return obj.user_id

    get_username.short_description = 'Username'

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        # if is superuser show all users
        if request.user.is_superuser:
            # self.list_filter = self.list_filter.append(branch_inputs.BranchInputFilter)
            return qs

        return qs.filter(user_id__branch_id=request.user.branch_id)


class WorkshopEvaluationAdmin(admin.ModelAdmin):

    list_display = ('id', 'get_topic_name', 'get_username',
                    'average', 'created_at', 'updated_at')

    list_filter = (general_inputs.AverageTextInputFilter,
                   general_inputs.UserTextInputFilter,
                   ("created_at", DateRangeQuickSelectListFilterBuilder()),)

    search_fields = ('id',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def get_username(self, obj):
        return obj.user_id

    get_username.short_description = 'Username'

    def get_topic_name(self, obj):
        return obj.topic_id

    get_topic_name.short_description = 'Topic name'

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        # if is superuser show all users
        if request.user.is_superuser:
            # self.list_filter = self.list_filter.append(branch_inputs.BranchInputFilter)
            return qs

        print(request.user.branch_id)

        return qs.filter(user_id__branch_id=request.user.branch_id)


class ScoreAdmin(admin.ModelAdmin):

    list_display = ('id', 'get_metric_name', 'score', 'simulation_id',
                    'get_username', 'created_at', 'updated_at')

    list_filter = (score_inputs.ScoreTextInputFilter,
                   score_inputs.ScoreUserTextInputFilter,
                   simulation_inputs.SimulationTextInputFilter,
                   ('created_at', DateRangeQuickSelectListFilterBuilder()),)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def get_username(self, obj):
        return obj.simulation_id.user_id

    get_username.short_description = 'Username'

    def get_metric_name(self, obj):
        return obj.metric_id

    get_metric_name.short_description = 'Metric name'


class MetricAdmin(admin.ModelAdmin):

    list_display = ('id', 'metric_name', 'created_at', 'updated_at')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(MetricModel, MetricAdmin)
admin.site.register(ScoreModel, ScoreAdmin)
admin.site.register(SimulationModel, SimulationAdmin)
admin.site.register(WorkshopEvaluationModel, WorkshopEvaluationAdmin)
