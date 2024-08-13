from drf_yasg import openapi


__author__ = 'Ricardo'
__version__ = '1.0'


# ----------------------------------------------------
#                      Responses
# ----------------------------------------------------


http_200_response = openapi.Response(
    description="Instrucciones recuperadas exitosamente",
    content={
        'application/json': {
            'example': {
                "instructions": "Aquí van las instrucciones detalladas de cómo evaluar la simulación y la conversación."
            }
        }
    }
)

http_404_response = openapi.Response(description="No autorizado", examples={
                                     'application/json': {'instructions': 'Debes de ...'}})
