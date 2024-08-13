from drf_yasg import openapi


__author__ = 'Ricardo'
__version__ = '1.0'


# ----------------------------------------------------
#                      Parameters
# ----------------------------------------------------


product_name_parameter = openapi.Parameter(
    'product_name',
    openapi.IN_QUERY,
    description="Nombre del producto",
    type=openapi.TYPE_STRING,
    required=True
)

customer_type_parameter = openapi.Parameter(
    'customer_type',
    openapi.IN_QUERY,
    description="Tipo de cliente",
    type=openapi.TYPE_STRING,
    required=True
)

document_names_parameter = openapi.Parameter(
    'document_names',
    openapi.IN_QUERY,
    description="Nombres de documentos que se quieren incluir en la simulación",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING),
    minItems=2,
    maxItems=2,
    required=True
)


# ----------------------------------------------------
#                      Responses
# ----------------------------------------------------


http_200_response = openapi.Response(
    description="Simulación personalizada generada exitosamente",
    content={
        'application/json': {
            'example': {
                "simulation": "Texto formateado de la simulación con todos los detalles relevantes."
            }
        }
    }
)

http_404_response = openapi.Response(
    description="No encontrado - Puede ser que el producto, cliente o documento no fueron encontrados")
