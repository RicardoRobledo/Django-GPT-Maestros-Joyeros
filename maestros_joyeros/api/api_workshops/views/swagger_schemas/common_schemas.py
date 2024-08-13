from drf_yasg import openapi


__author__ = 'Ricardo'
__version__ = '1.0'


# ----------------------------------------------------
#                      Parameters
# ----------------------------------------------------


document_name_parameter = openapi.Parameter(
    'document_name',
    openapi.IN_PATH,
    description="Nombre de un documento",
    type=openapi.TYPE_STRING,
    required=True
)
