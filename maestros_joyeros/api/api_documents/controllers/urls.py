from django.urls import path

from ..views.api_document_views import get_document


app_name = 'api_documents'


urlpatterns = [
    path('document/<str:document_name>/', get_document, name='get_document'),
]
