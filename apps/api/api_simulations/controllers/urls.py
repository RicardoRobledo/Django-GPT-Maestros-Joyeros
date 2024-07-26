from django.urls import path
from ..views import api_simulation_views


urlpatterns = [
    path('simulation/', api_simulation_views.get_simulation),
    path('simulation/custom_simulation/', api_simulation_views.get_custom_simulation),
    path('simulation/customer_type/<str:customer_type>', api_simulation_views.get_type_based_simulation),
    path('simulation/evaluation/', api_simulation_views.save_evaluation),
    path('simulation/evaluation/instructions/', api_simulation_views.retrieve_instructions),
]
