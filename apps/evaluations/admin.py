from django.contrib import admin

from .models import MetricModel, ScoreModel, SimulationModel, WorkshopEvaluationModel


admin.site.register(MetricModel)
admin.site.register(ScoreModel)
admin.site.register(SimulationModel)
admin.site.register(WorkshopEvaluationModel)
