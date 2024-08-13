from drf_yasg import openapi


__author__ = 'Ricardo'
__version__ = '1.0'


# ----------------------------------------------------
#                      Parameters
# ----------------------------------------------------


gettbs_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        '4Cs': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bien el vendedor cumple con ser claro, conciso, coherente y cordial",
            minimum=1,
            maximum=10
        ),
        'Ortografía': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bien el vendedor cumple con tener buena ortografía",
            minimum=1,
            maximum=10
        ),
        'Redacción': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bien el vendedor tiene buena redacción",
            minimum=1,
            maximum=10
        ),
        'Promueve_acción': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bien el vendedor promueve a la acción de compra",
            minimum=1,
            maximum=10
        ),
        'No_forzado': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bueno es el vendedor para no forzar compras",
            minimum=1,
            maximum=10
        ),
        'Sinceridad': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bueno es el vendedor para ser sincero",
            minimum=1,
            maximum=10
        ),
        'Empatía': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bueno es el vendedor para ser empático",
            minimum=1,
            maximum=10
        ),
        'Iniciativa': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bueno es el vendedor para tener iniciativa",
            minimum=1,
            maximum=10
        ),
        'Seguimiento': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bueno es el vendedor para hacer seguimiento",
            minimum=1,
            maximum=10
        ),
        'Cierre_conversación': openapi.Schema(
            type=openapi.TYPE_NUMBER,
            description="Calificación que indica que tan bueno es el vendedor para cerrar conversaciones",
            minimum=1,
            maximum=10
        ),
        'Conversación': openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Conversación de la última simulación que hizo el usuario"
        ),
    },
    required=[
        '4Cs', 'Ortografía', 'Redacción', 'Promueve_acción', 'No_forzado',
        'Sinceridad', 'Empatía', 'Iniciativa', 'Seguimiento', 'Cierre_conversación', 'Conversación'
    ]
)


# ----------------------------------------------------
#                      Responses
# ----------------------------------------------------


http_200_response = openapi.Response(
    description="Evaluación guardada exitosamente",
    examples={
        'application/json': {
            "msg": "Evaluation of simulation saved successfully"
        }
    }
)

http_401_response = openapi.Response(
    description="No autorizado")

http_406_response = openapi.Response(
    description="Las claves de las métricas no son correctas o la conversación no ha sido proporcionada")
