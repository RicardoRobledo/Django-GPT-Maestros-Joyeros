from drf_yasg import openapi


__author__ = 'Ricardo'
__version__ = '1.0'


# ----------------------------------------------------
#                      Responses
# ----------------------------------------------------


http_200_response = openapi.Response(
    description="Simulación base generada exitosamente",
    content={
        'application/json': {
            'example': {
                "simulation": "Texto formateado de la simulación con el contexto esencial."
            }
        }
    }
)


http_404_response = openapi.Response(description="No autorizado")
