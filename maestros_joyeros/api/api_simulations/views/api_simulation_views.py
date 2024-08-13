from datetime import timedelta

from django.utils import timezone

from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from drf_yasg.utils import swagger_auto_schema

from maestros_joyeros.api.api_simulations.utils.evaluation_handlers import save_simulation_evaluation
from maestros_joyeros.users.models import UserModel
from maestros_joyeros.documents.models import DocumentModel
from maestros_joyeros.customers.models import CustomerModel
from maestros_joyeros.products.models import ProductModel
from maestros_joyeros.evaluations.models import MetricModel
from maestros_joyeros.users.utils import user_handlers

from ...api_customers.utils.customer_handlers import get_random_customer
from ...api_products.utils.product_handlers import prepare_product
from ...api_documents.utils.document_handlers import get_context_documents

from ..utils.prompt_handlers import read_prompt, format_simulation_prompt

from .swagger_schemas import (
    save_evaluation_schemas,
    retrieve_instructions_schemas,
    get_custom_simulation_schemas,
    get_simulation_schemas,
    get_type_based_simulation_schemas
)


__author__ = 'Ricardo'
__version__ = '1.0'


# -----------------------------


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene una simulación para evaluar las habilidades del vendedor",
    operation_id="GetTestSale",
    responses={
        status.HTTP_200_OK: get_simulation_schemas.http_200_response,
        status.HTTP_404_NOT_FOUND: get_simulation_schemas.http_404_response,
    },
    tags=['Simulations']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_simulation(request):
    """
    This view return us a random simulation of a sale
    """

    # print(GPTTokenObtainPairSerializer(request.auth))
    # Obtener la fecha y hora actual
    # now = timezone.now()

    # Calcular la fecha de hace 32 días
    # start_date = now - timedelta(days=32)

    # import random
    # for i in TopicModel.objects.all():
    #    EvaluationModel.objects.create(average=random.randint(0,10), topic_id=i, user_id=user)

    product = prepare_product()
    customer = get_random_customer()
    documents = get_context_documents()

    formatted_output = format_simulation_prompt(
        'maestros_joyeros/api/api_simulations/schemas/prompt_simulation.txt', product, customer, documents)
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'simulation': formatted_output}, content_type='application/json', status=status.HTTP_200_OK)


# -----------------------------


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene una simulación personalizada para evaluar las habilidades del vendedor",
    operation_id="GetCustomTestSale",
    manual_parameters=[
        get_type_based_simulation_schemas.product_name_parameter,
        get_type_based_simulation_schemas.customer_type_parameter,
        get_type_based_simulation_schemas.document_names_parameter
    ],
    responses={
        status.HTTP_200_OK: get_type_based_simulation_schemas.http_200_response,
        status.HTTP_404_NOT_FOUND: get_type_based_simulation_schemas.http_404_response,
    },
    tags=['Simulations']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_type_based_simulation(request):
    """
    This view return us a simulation of a sale based in types

    :param profile: str of a customer type
    """

    document_names = request.query_params.getlist('document_names')
    customer_type = request.query_params.get('customer_type')
    product_name = request.query_params.get('product_name')

    documents = DocumentModel.objects.filter(
        document_name__in=document_names, for_simulation=True)

    if not documents.count() == 2:
        raise NotFound('There is a document that was not found')

    customer = CustomerModel.objects.filter(customer_type=customer_type)

    if not customer.exists():
        raise NotFound('Customer was not found')

    customer = customer.first()
    product = ProductModel.objects.filter(product_name=product_name)

    if not product.exists():
        raise NotFound('Product was not found')

    product = product.first()

    formatted_output = format_simulation_prompt(
        'maestros_joyeros/api/api_simulations/schemas/prompt_simulation.txt', product, customer, documents)
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'simulation': formatted_output}, content_type='application/json', status=status.HTTP_200_OK)


# -----------------------------


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene una simulación base para evaluar las habilidades del vendedor una vez se haya descrito la información",
    operation_id="GetCustomTestSaleBase",
    responses={
        status.HTTP_200_OK: get_custom_simulation_schemas.http_200_response,
        status.HTTP_404_NOT_FOUND: get_custom_simulation_schemas.http_404_response,
    },
    tags=['Simulations']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_custom_simulation(request):
    """
    This view return us a custom simulation with the most essential context

    :param profile: str of a customer profile
    """

    product = prepare_product()
    documents = get_context_documents()

    formatted_output = format_simulation_prompt(
        'maestros_joyeros/api/api_simulations/schemas/prompt_custom_simulation.txt', product, None, documents)
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'simulation': formatted_output}, content_type='application/json', status=status.HTTP_200_OK)


# -----------------------------


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene instrucciones a seguir de cómo evaluar la simulación y conversación",
    operation_id="GetInstructionsEvaluation",
    responses={
        status.HTTP_200_OK: retrieve_instructions_schemas.http_200_response,
        status.HTTP_404_NOT_FOUND: retrieve_instructions_schemas.http_404_response,
    },
    tags=['Simulations']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_instructions(request):

    instructions = read_prompt(
        'maestros_joyeros/api/api_simulations/schemas/prompt_evaluation_instructions.txt')

    return Response({'instructions': instructions}, content_type='application/json', status=status.HTTP_200_OK)


# -----------------------------


@swagger_auto_schema(
    method='post',
    operation_description="Envía el resultado de evaluación de la conversación en base a métricas para ser guardada en base de datos",
    operation_id="PostTestSale",
    request_body=save_evaluation_schemas.gettbs_request_body,
    responses={
        status.HTTP_200_OK: save_evaluation_schemas.http_200_response,
        status.HTTP_406_NOT_ACCEPTABLE: save_evaluation_schemas.http_406_response,
        status.HTTP_401_UNAUTHORIZED: save_evaluation_schemas.http_401_response,
    },
    tags=['Simulations']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_evaluation(request):

    evaluations_gotten = request.data

    are_metrics_correct = [
        metric.metric_name == evaluation
        for metric, evaluation in zip(MetricModel.objects.all(), evaluations_gotten)
    ]

    if not all(are_metrics_correct):
        user_handlers.register_action(
            request=request, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        raise NotAcceptable('The metric keys are not correct')

    conversation = evaluations_gotten.pop('Conversación', None)

    if not conversation:
        user_handlers.register_action(
            request=request, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        raise NotAcceptable('The conversation has not been provided')

    # Getting the user
    user = UserModel.objects.filter(id=request.auth['user_id']).first()

    save_simulation_evaluation(user, evaluations_gotten, conversation)
    user_handlers.register_action(
        request=request, status_code=status.HTTP_200_OK)

    return Response({'msg': 'Evaluation of simulation saved succesfully'}, content_type='application/json', status=status.HTTP_200_OK)
