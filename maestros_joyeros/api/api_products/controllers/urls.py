from django.urls import path

from ..views import api_product_views


app_name = 'api_products'


urlpatterns = [
    path('', api_product_views.get_products, name='product-list'),
    path('product/<str:product_name>',
         api_product_views.get_product, name='product-detail'),
]
