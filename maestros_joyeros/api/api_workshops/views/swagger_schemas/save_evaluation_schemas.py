from drf_yasg import openapi


__author__ = 'Ricardo'
__version__ = '1.0'


# ----------------------------------------------------
#                     Parameters
# ----------------------------------------------------


topic_name_parameter = openapi.Parameter(
    'topic_name',
    openapi.IN_PATH,
    description="Nombre de un tema",
    type=openapi.TYPE_STRING,
    required=True
)


average_parameter = openapi.Parameter(
    'Average',
    openapi.IN_FORM,
    description="Calificación que indica que tan bien ha respondido el vendedor a una pregunta de un taller",
    type=openapi.TYPE_NUMBER,
    required=True,
    minimum=1,
    maximum=10
)


# ----------------------------------------------------
#                      Responses
# ----------------------------------------------------


http_200_response = openapi.Response(
    description="Evaluación del taller guardada exitosamente",
    content={
        'application/json': {
            'example': {
                "msg": "Evaluation of workshop saved successfully"
            }
        }
    }
)

http_406_response = openapi.Response(
    description="El promedio no ha sido proporcionado o el tema no fue encontrado")
http_401_response = openapi.Response(description="No autorizado")
