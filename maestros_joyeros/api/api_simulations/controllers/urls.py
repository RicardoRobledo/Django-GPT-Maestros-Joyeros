from django.urls import path
from ..views import api_simulation_views


app_name = 'api_simulations'


urlpatterns = [
    path('simulation/', api_simulation_views.get_simulation, name='get_simulation'),
    path('simulation/custom_simulation_base/',
         api_simulation_views.get_custom_simulation, name='get_custom_simulation'),
    path('simulation/custom_simulation/',
         api_simulation_views.get_type_based_simulation, name='get_type_based_simulation'),
    path('simulation/evaluation/',
         api_simulation_views.save_evaluation, name='save_evaluation'),
    path('simulation/evaluation/instructions/',
         api_simulation_views.retrieve_instructions, name='retrieve_instructions'),
]
