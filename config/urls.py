"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView
)
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .support_views import swagger_logout


schema_view = get_schema_view(
    openapi.Info(
        title="Maestros Joyeros API",
        default_version='v1',
        description="Esta es la api que conecta con el GPT de maestros joyeros. Esta API es la encargada de gestionar los datos de los vendedores y consultar informacion, para capacitación y simulacion de ventas con los vendedores. Los principales recursos que maneja son: productos, documentos, simulaciones, talleres y clientes.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)


api_prefix = 'api/v1'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('maestros_joyeros.authentication.controllers.urls')),

    path(f'{api_prefix}/simulations/',
         include('maestros_joyeros.api.api_simulations.controllers.urls')),
    path(f'{api_prefix}/workshops/',
         include('maestros_joyeros.api.api_workshops.controllers.urls')),
    path(f'{api_prefix}/customers/',
         include('maestros_joyeros.api.api_customers.controllers.urls')),
    path(f'{api_prefix}/products/',
         include('maestros_joyeros.api.api_products.controllers.urls')),
    path(f'{api_prefix}/documents/',
         include('maestros_joyeros.api.api_documents.controllers.urls')),
    path(f'{api_prefix}/authentication/',
         include('maestros_joyeros.api.api_authentication.controllers.urls')),

    path('api-auth/', include('rest_framework.urls')),
    path('swagger-api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('swagger-api/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/logout/', swagger_logout, name='swagger-logout'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

handler404 = 'maestros_joyeros.authentication.views.authentication_views.custom_404'
