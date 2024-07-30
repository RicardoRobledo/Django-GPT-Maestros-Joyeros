from django.contrib import admin

from .models import MetricModel, ScoreModel, SimulationModel, WorkshopEvaluationModel


class SimulationAdmin(admin.ModelAdmin):

    list_display = ('id', 'user_id', 'average', 'created_at', 'updated_at')

    search_fields = ('id', 'user_id__username') 

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields


class WorkshopEvaluationAdmin(admin.ModelAdmin):

    list_display = ('id', 'topic_id', 'user_id', 'average', 'created_at', 'updated_at')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields


class ScoreAdmin(admin.ModelAdmin):

    list_display = ('id', 'metric_id', 'score', 'created_at', 'updated_at')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
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


admin.site.register(MetricModel, MetricAdmin)
admin.site.register(ScoreModel, ScoreAdmin)
admin.site.register(SimulationModel, SimulationAdmin)
admin.site.register(WorkshopEvaluationModel, WorkshopEvaluationAdmin)
