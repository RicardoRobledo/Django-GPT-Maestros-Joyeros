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

    list_display = ('id', 'user_id', 'average', 'created_at', 'updated_at')

    list_filter = (general_inputs.AverageTextInputFilter,
                   general_inputs.UserTextInputFilter,
                   ("created_at", DateRangeQuickSelectListFilterBuilder()),)

    #search_fields = ('id', 'user_id__username')
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


class WorkshopEvaluationAdmin(admin.ModelAdmin):

    list_display = ('id', 'topic_id', 'user_id',
                    'average', 'created_at', 'updated_at')

    list_filter = (general_inputs.AverageTextInputFilter, ("created_at", DateRangeQuickSelectListFilterBuilder()),)

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


class ScoreAdmin(admin.ModelAdmin):

    list_display = ('id', 'metric_id', 'score', 'simulation_id',
                    'username', 'created_at', 'updated_at')

    list_filter = (score_inputs.ScoreTextInputFilter,
                   score_inputs.ScoreUserTextInputFilter,
                   simulation_inputs.SimulationTextInputFilter,
                   ('created_at', DateRangeQuickSelectListFilterBuilder()),)

    def username(self, obj):
        return obj.simulation_id.user_id

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
