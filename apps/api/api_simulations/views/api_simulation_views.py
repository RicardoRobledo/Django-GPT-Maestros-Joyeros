from datetime import timedelta

from django.utils import timezone

from rest_framework.exceptions import NotAcceptable
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view

from apps.evaluations.utils.evaluation_handlers import save_simulation_evaluation
from apps.users.models import UserModel
from apps.evaluations.models import MetricModel

from apps.users.utils import user_handlers
from ..utils.customer_handlers import get_customer, get_random_customer
from ..utils.document_handlers import prepare_product
from ..utils.prompt_handlers import format_prompt


__author__ = 'Ricardo'
__version__ = '1.0'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_simulation(request):
    """ 
    This view return us a simulation of a sale
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

    formatted_output = format_prompt('apps/api/api_simulations/schemas/prompt_simulation.txt', product, customer)
    user_handlers.register_action(request=request, status_code=status.HTTP_200_OK)

    return Response({'simulation':formatted_output}, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_type_based_simulation(request, customer_type:str):
    """
    This view return us a simulation of a sale based in a customer type

    :param profile: str of a customer type
    """

    product = prepare_product()
    customer = get_customer(customer_type)

    formatted_output = format_prompt('apps/api/api_simulations/schemas/prompt_simulation.txt', product, customer)

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
    formatted_output = format_prompt('apps/api/api_simulations/schemas/prompt_custom_simulation.txt', product)

    user_handlers.register_action(request=request, status_code=status.HTTP_200_OK)

    return Response({'simulation':formatted_output}, content_type='application/json', status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_instructions(request):

    inst = """
Despues debes de tomar en cuenta el documento de procedimientos y evaluar con las instrucciones que están en el documento de procedimientos.

Cuando se termine una simulación debes de asumir el rol de un evaluador de vendedores.

Criterios de evaluación: Tono, que puede hacer, que no, información de comportamiento y de la empresa, calidad del servicio, negociación, proceso de ventas, oferta de servicios y capacidades, política de comisiones, cambios y devoluciones de productos, cancelaciones, disponibilidad y existencia, envíos y entregas aseguradas, facturación, forma de pago, garantía, orden de compra digital, precios, productos y servicios, promociones y cupones, quejas y reclamaciones, reembolso de dinero, seguridad, suscripción o registro de nuevos usuarios por internet, si el vendedor se ha inventado información que no está en el documento, si se equivoca en proporcionar datos que son erróneos.

Debes seguir los siguientes pasos:
1.- Hacer una evaluación estricta analizando la simulación que tuvo el vendedor y la información de procedimientos en base a los criterios de evaluación.
2.- Dar retroalimentación estricta analizando la simulación que tuvo el vendedor y la información de procedimientos considerando los criterios de evaluación diciendo en que se equivocó y que debe de hacer.
3.- Enviar la información de la evaluación con el action de enviar evaluación.

# Ejemplos
Ejemplo de cómo puedes iniciar la simulación con intención de compra:
    - Buen día, estuve viendo por instagram unos lentes que me interesaron, ¿Puede darme detalles de ellos?.
    - ¿Qué tal?, estuve viendo los Huggies que venden y me parecen interesantes, ¿Qué precio tienen?.

Ejemplo de como puedes debes iniciar la simulación con intención de queja:
    - Espero que tenga un buen día, compré unos aretes en Maestros Joyeros y estoy inconforme con ellos, ¿Que se puede hacer?.
    - Saludos, tengo unos lentes que compré con ustedes y estoy insatisfecho, me temo que se desprendió una joya, ¿Pueden ayudarme?.

Ejemplo de cómo debes evaluar una simulación, debes de evaluar leyendo toda la conversación de la simulación y leyendo toda la información obtenida de los procedimientos para al final comparar:
   *leeré toda la información de procedimientos y la conversación de la simulación para poder evaluar y retroalimentar*
    1.- En la conversación empezaste diciendo '¿Qué onda?' hablando de manera informal lo cual es incorrecto. Este es un ejemplo de cómo debes saludar que se menciona en la información obtenida de los procedimientos:
    Buenas tardes, te atiende tu asesor joyero José Pérez y te acompañaré en tu proceso de compra, ¿cómo te puedo ayudar?.
    2.- No se especifica en la información obtenida de los procedimientos que los anillos tengan adornos con zafiros, solo con rubíes, de igual modo mencionaste que pintamos joyas, 
    pero no hacemos pintado de joyas, solo grabado en láser.
    3.- Se dijo que al final del proceso de personalización de una joya se empaca y se entrega, pero en la información obtenida de los procedimientos hay un paso extra al final y es que se realiza un protocolo de posventa en el proceso final.
    4.- Se mencionó que el cliente tiene un plazo de 30 días para un cambio de producto, pero la información obtenida de los procedimientos dice que son 40 días.
    5.- El vendedor mencionó  al cliente que estaba dentro del plazo que se hacen devoluciones, sin embargo en la información obtenida de los procedimientos se menciona que son 14 días y no 30.
    6.- Mencionaste que ofrecemos descuentos, sin embargo en la información obtenida de los procedimientos se menciona que no ofrecemos.
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
