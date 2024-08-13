from drf_yasg import openapi


__author__ = 'Ricardo'
__version__ = '1.0'


# ----------------------------------------------------
#                      Resposes
# ----------------------------------------------------


http_200_response = openapi.Response(
    description="Taller específico obtenido exitosamente",
    content={
        'application/json': {
            'example': {
                "document": "Contenido del documento específico.",
                "topic": "Nombre del tema relacionado con el documento."
            }
        }
    }
)

http_404_response = openapi.Response(description="Documento no encontrado")

http_401_response = openapi.Response(description="No autorizado")
