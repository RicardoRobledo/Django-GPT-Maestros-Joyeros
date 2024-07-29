from datetime import timedelta

from django.utils import timezone

from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from apps.api.api_simulations.utils.evaluation_handlers import save_simulation_evaluation
from apps.users.models import UserModel
from apps.documents.models import DocumentModel
from apps.customers.models import CustomerModel
from apps.products.models import ProductModel
from apps.evaluations.models import MetricModel

from apps.users.utils import user_handlers
from ...api_customers.utils.customer_handlers import get_random_customer
from ...api_products.utils.product_handler import prepare_product
from ...api_documents.utils.document_handlers import get_context_documents

from ..utils.prompt_handlers import format_prompt


__author__ = 'Ricardo'
__version__ = '1.0'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_simulation(request):
    """
    This view return us a random simulation of a sale
    """

    #print(GPTTokenObtainPairSerializer(request.auth))
    # Obtener la fecha y hora actual
    #now = timezone.now()

    # Calcular la fecha de hace 32 días
    #start_date = now - timedelta(days=32)

    #import random
    #for i in TopicModel.objects.all():
    #    EvaluationModel.objects.create(average=random.randint(0,10), topic_id=i, user_id=user)

    product = prepare_product()
    customer = get_random_customer()
    documents = get_context_documents()

    formatted_output = format_prompt('apps/api/api_simulations/schemas/prompt_simulation.txt', product, customer, documents)
    user_handlers.register_action(request=request, status_code=status.HTTP_200_OK)

    return Response({'simulation':formatted_output}, content_type='application/json', status=status.HTTP_200_OK)


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

    documents = DocumentModel.objects.filter(document_name__in=document_names, for_simulation=True)

    if not documents.count()==2:
        raise NotFound('There is a document that was not found')

    customer = CustomerModel.objects.filter(customer_type=customer_type)

    if not customer.exists():
        raise NotFound('Customer was not found')

    customer = customer.first()
    product = ProductModel.objects.filter(product_name=product_name)

    if not product.exists():
        raise NotFound('Product was not found')

    product = product.first()

    formatted_output = format_prompt('apps/api/api_simulations/schemas/prompt_simulation.txt', product, customer, documents)
    user_handlers.register_action(request=request, status_code=status.HTTP_200_OK)

    return Response({'simulation':formatted_output}, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_custom_simulation(request):
    """
    This view return us a custom simulation with the most essential context

    :param profile: str of a customer profile
    """

    product = prepare_product()
    documents = get_context_documents()

    formatted_output = format_prompt('apps/api/api_simulations/schemas/prompt_custom_simulation.txt', product, None, documents)
    user_handlers.register_action(request=request, status_code=status.HTTP_200_OK)

    return Response({'simulation':formatted_output}, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_instructions(request):

    inst = """
Debes de hacer lo siguiente:
1.- Hacer una evaluación estricta analizando la simulación que tuvo el vendedor y la información de simulación, la información de la simulación es lo verdadero, considéralo por si el vendedor lo contradice en la conversación a lo que dice en la información de la simulación, si lo hace es que está mal.
2.- Dar retroalimentación estricta analizando la conversación de la simulación que tuvo el vendedor y los documentos de contexto y el producto en la información de la simulación diciendo en que se equivocó, que debe de hacer, si se equivocó en un paso de un procedimiento dile como es, la información de la simulación es lo verdadero, considéralo por si el vendedor lo contradice en la conversación a lo que dice en la información de la simulación, si lo hace es que está mal.
3.- Enviar la información de la evaluación con el action de enviar evaluación.

La información está en formato de markdown donde los titulos empieza por el signo '#' y los subtitulos inicias con el signo '####'.

Ejemplo de cómo debes retroalimentar la simulación, debes de evaluar leyendo toda la conversación de la simulación y leer toda la información obtenida de la simulación considerando productos y documentos de contexto para comparar:
   *leeré toda la información de la simulación obtenida y la conversación de la simulación para poder retroalimentar*
    1.- En la conversación empezaste diciendo '¿Qué onda?' hablando de manera informal lo cual es incorrecto. Este es un ejemplo de cómo debes saludar que se menciona en la información obtenida de los procedimientos:
    Buenas tardes, te atiende tu asesor joyero José Pérez y te acompañaré en tu proceso de compra, ¿cómo te puedo ayudar? - Referencia: Información de empresa y comportamiento.
    2.- El vendedor mencionó  al cliente que estaba dentro del plazo que se hacen devoluciones, sin embargo en la información obtenida de los procedimientos se menciona que son (x número) de días y no (otro número) de días - Referencia: Cambios y devoluciones.
    3.- No se especifica en la información obtenida de la simulación que los anillos tengan adornos con zafiros, solo con rubíes, de igual modo mencionaste que pintamos joyas, 
    pero no hacemos pintado de joyas, solo grabado en láser - Referencia: Proceso de fabricación.
    4.- Se dijo que al final del proceso de personalización de una joya se empaca y se entrega, pero en la información obtenida de  la simulación hay un paso extra al final y es que se realiza un protocolo de posventa en el proceso final - Referencia: Personalización.
    5.- Se mencionó que el cliente tiene un plazo de (x número) de días para un cambio de producto, pero la información obtenida de la simulación dice que son (otro número) de días - Referencia: Cambios y devoluciones.
    6.- Para la compra hiciste el proceso de generar un enlace de pago, se lo enviaste y le dijiste las promociones de productos parecidos, sin embargo el proceso es: pedir anticipo, generar enlace de pago, el cliente debe generar una solicitud y posteriormente decir las promociones de productos parecidos. Esto es el proceso que se menciona en la información obtenida de la simulación - Referencia: Proceso de ventas.
    7.- Mencionaste que la cadena de oro Raymond es de (x número) kilates, pero en la información obtenida de la simulación dice que es de (otro número) de kilates - Referencia: Producto cadena.
    8.- Mencionaste que los datos necesarios para la factura son el nombre y teléfono, pero en la información obtenida de la simulación dice que son nombre, dirección, teléfono y correo - Referencia: Facturación.
    ... así debes de evaluar todo hasta que se cubra toda la conversación de la simulación y como se apega con la información de procedimientos.    
"""
    return Response({'instructions':inst}, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_evaluation(request):

    evaluations_gotten = request.data

    are_metrics_correct = [
        metric.metric_name==evaluation
        for metric, evaluation in zip(MetricModel.objects.all(), evaluations_gotten)
    ]

    if not all(are_metrics_correct):
        user_handlers.register_action(request=request, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        raise NotAcceptable('The metric keys are not correct')
    
    conversation = evaluations_gotten.pop('Conversación', None)

    if not conversation:
        user_handlers.register_action(request=request, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        raise NotAcceptable('The conversation has not been provided')

    # Getting the user
    user = UserModel.objects.filter(id=request.auth['user_id']).first()

    save_simulation_evaluation(user, evaluations_gotten, conversation)
    user_handlers.register_action(request=request, status_code=status.HTTP_200_OK)

    return Response({'msg':'Evaluation of simulation saved succesfully'}, content_type='application/json', status=status.HTTP_200_OK)
