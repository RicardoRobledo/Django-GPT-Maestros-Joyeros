from drf_yasg import openapi


__author__ = 'Ricardo'
__version__ = '1.0'


# ----------------------------------------------------
#                      Responses
# ----------------------------------------------------


http_200_response = openapi.Response(
    description="Taller obtenido exitosamente",
    content={
        'application/json': {
            'example': {
                "document": "Contenido del documento seleccionado.",
                "topic": "Nombre del tema relacionado con el documento."
            }
        }
    }
)

http_404_response = openapi.Response(description="No se encontró el taller")

http_401_response = openapi.Response(description="No autorizado")