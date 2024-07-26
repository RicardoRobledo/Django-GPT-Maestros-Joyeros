from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ..views.api_authentication_views import generate_gpt_tokens


urlpatterns = [
    path('token/', generate_gpt_tokens, name='generate_gpt_tokens'),
]
