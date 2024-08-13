from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
import random

from datetime import timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from drf_yasg.utils import swagger_auto_schema

from maestros_joyeros.users.models import UserModel
from maestros_joyeros.documents.models import DocumentModel, TopicModel
from maestros_joyeros.users.utils import user_handlers

from ...api_documents.utils.document_handlers import get_documents_not_evaluated
from ...api_workshops.utils.evaluation_handlers import sum_averages_evaluations

from ..utils.evaluation_handlers import save_workshop_evaluation

from .swagger_schemas import (
    common_schemas,
    get_workshop_schemas,
    get_specific_workshop_schemas,
    save_evaluation_schemas
)


__author__ = 'Ricardo'
__version__ = '0.1'


# ------------------------------


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene un taller",
    operation_id="GetWorkshop",
    responses={
        status.HTTP_200_OK: get_workshop_schemas.http_200_response,
        status.HTTP_404_NOT_FOUND: get_workshop_schemas.http_404_response,
        status.HTTP_401_UNAUTHORIZED: get_workshop_schemas.http_401_response,
    },
    tags=['Workshops']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workshop(request):
    """
    This view get a random workshop
    """

    # print(GPTTokenObtainPairSerializer(request.auth))
    # Get actual date and hour
    now = timezone.now()

    # Calculate date 32 days ago
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
        topics_evaluated_with_average = sum_averages_evaluations(
            user, start_date)

        documents = DocumentModel.objects.filter(
            topic_id__in=[topic_evaluated_with_average['topic_id']
                          for topic_evaluated_with_average in topics_evaluated_with_average],
            for_workshop=True
        )

        document_selected = random.choice(documents)

    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'document': document_selected.content, 'topic': document_selected.topic_id.topic_name}, content_type='application/json', status=status.HTTP_200_OK)


# ------------------------------


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene un taller en base a un documento específico",
    operation_id="GetSpecificWorkshop",
    manual_parameters=[common_schemas.document_name_parameter],
    responses={
        status.HTTP_200_OK: get_specific_workshop_schemas.http_200_response,
        status.HTTP_404_NOT_FOUND: get_specific_workshop_schemas.http_404_response,
        status.HTTP_401_UNAUTHORIZED: get_specific_workshop_schemas.http_401_response,
    },
    tags=['Workshops']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser])
def get_specific_workshop(request, document_name):
    """
    This view get a specific workshop
    """

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


# ------------------------------


evaluation_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "Average": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bien ha respondido el vendedor a una pregunta de un taller",
            minimum=1,
            maximum=10
        )
    },
)


@swagger_auto_schema(
    method='post',
    operation_description="Envía el resultado de la evaluación del taller",
    operation_id="PostTestSale",
    request_body=evaluation_request_body,
    responses={
        status.HTTP_200_OK: save_evaluation_schemas.http_200_response,
        status.HTTP_406_NOT_ACCEPTABLE: save_evaluation_schemas.http_406_response,
        status.HTTP_401_UNAUTHORIZED: save_evaluation_schemas.http_401_response
    },
    tags=['Workshops']
)
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
        raise NotAcceptable('The topic was not found')

    # Getting the user
    user = UserModel.objects.filter(id=request.auth['user_id']).first()

    save_workshop_evaluation(user, average, topic.first())
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'msg': 'Evaluation of workshop saved succesfully'}, content_type='application/json', status=status.HTTP_200_OK)
