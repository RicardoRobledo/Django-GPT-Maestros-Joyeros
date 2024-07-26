from django.urls import path

from ..views import api_product_views


urlpatterns = [
    path('', api_product_views.get_products),
    path('product/<str:product_name>', api_product_views.get_product),
]
