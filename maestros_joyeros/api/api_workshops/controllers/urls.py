from django.urls import path

from ..views import api_workshop_views


app_name = 'api_workshops'


urlpatterns = [
    path('workshop/', api_workshop_views.get_workshop, name='get_workshop'),
    path('workshop/<str:document_name>',
         api_workshop_views.get_specific_workshop, name='get_specific_workshop'),
    path('workshop/evaluation/<str:topic_name>',
         api_workshop_views.save_evaluation, name='save_evaluation'),
]
