from rest_framework import status
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from ...api_documents.utils.document_handlers import get_documents_not_evaluated
from ...api_workshops.utils.evaluation_handlers import sum_averages_evaluations
from maestros_joyeros.users.models import UserModel
from maestros_joyeros.documents.models import DocumentModel, TopicModel

from datetime import timedelta
from django.utils import timezone

from maestros_joyeros.users.utils import user_handlers
from ..utils.evaluation_handlers import save_workshop_evaluation


__author__ = 'Ricardo'
__version__ = '0.1'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workshop(request):
    """
    This view get our products
    """

    # print(GPTTokenObtainPairSerializer(request.auth))
    # Obtener la fecha y hora actual
    now = timezone.now()

    # Calcular la fecha de hace 32 días
    start_date = now - timedelta(days=32)

    user = UserModel.objects.filter(id=request.auth['user_id']).first()

    documents_not_evaluated = get_documents_not_evaluated(
        user, start_date, for_workshop=True)
    document_selected = None

    if documents_not_evaluated.exists():

        document_not_evaluated = documents_not_evaluated.first()

        document_selected = DocumentModel.objects.filter(
            id=document_not_evaluated['id'],
            for_workshop=True
        ).first()

    else:
        # doing a sum of averages with the evaluations and return the document with the lowest average
        document_selected = sum_averages_evaluations(user, start_date)[0]

    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'document': document_selected.content, 'topic': document_selected.topic_id.topic_name}, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_specific_workshop(request, document_name):
    """
    This view get a specific workshop
    """

    # Getting the user
    user = UserModel.objects.filter(id=request.auth['user_id']).first()

    # Getting the document
    document = DocumentModel.objects.filter(
        for_workshop=True, document_name=document_name)

    if not document.exists():
        user_handlers.register_action(
            request=request, status_code=status.HTTP_404_NOT_FOUND)
        raise NotFound('The document was not found')

    document_gotten = document.first()
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'document': document_gotten.content, 'topic': document_gotten.topic_id.topic_name}, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_evaluation(request, topic_name):
    """
    This view save the evaluation of the workshop
    """

    # Getting average
    average = request.data.pop('Average', None)

    if not average:
        user_handlers.register_action(
            request=request, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        raise NotAcceptable('The average has not been provided')

    # Getting the topic
    topic = TopicModel.objects.filter(topic_name=topic_name)

    if not topic.exists():
        user_handlers.register_action(
            request=request, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        raise NotFound('The topic was not found')

    # Getting the user
    user = UserModel.objects.filter(id=request.auth['user_id']).first()

    save_workshop_evaluation(user, average, topic.first())
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'msg': 'Evaluation of workshop saved succesfully'}, content_type='application/json', status=status.HTTP_200_OK)
