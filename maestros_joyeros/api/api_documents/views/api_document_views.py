from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from maestros_joyeros.documents.models import DocumentModel
from maestros_joyeros.users.utils import user_handlers

from ..serializers.document_serializers import DocumentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document(request, document_name):
    """
    This view get a document
    """

    document = DocumentModel.objects.filter(document_name=document_name)

    if not document.exists():

        user_handlers.register_action(
            request=request, status_code=status.HTTP_404_NOT_FOUND)

        return Response({'document': 'document not found'}, content_type='application/json', status=status.HTTP_404_NOT_FOUND)

    else:

        document_serialized = DocumentSerializer(document.first())
        user_handlers.register_action(
            request=request, status_code=status.HTTP_200_OK)

        return Response({'document': document_serialized.data}, content_type='application/json', status=status.HTTP_200_OK)
