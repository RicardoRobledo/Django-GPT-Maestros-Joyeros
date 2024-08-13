from django.urls import path
from ..views.api_authentication_views import generate_gpt_tokens, swagger_logout


app_name = 'api_authentication'


urlpatterns = [
    path('token/', generate_gpt_tokens, name='generate_gpt_tokens'),
    path('swagger/logout/', swagger_logout, name='swagger-logout'),
]
