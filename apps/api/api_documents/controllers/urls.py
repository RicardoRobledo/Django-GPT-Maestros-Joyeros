from django.urls import path

from ..views.api_document_views import get_document


urlpatterns = [
    path('document/<str:document_name>/', get_document),
]
