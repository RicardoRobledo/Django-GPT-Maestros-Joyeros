from django.contrib import admin

from .models import MetricModel, ScoreModel, SimulationEvaluationModel, WorkshopEvaluationModel


admin.site.register(MetricModel)
admin.site.register(ScoreModel)
admin.site.register(SimulationEvaluationModel)
admin.site.register(WorkshopEvaluationModel)
