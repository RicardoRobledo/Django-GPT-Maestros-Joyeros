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
    TokenRefreshView,
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
    path(f'{api_prefix}/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

handler404 = 'maestros_joyeros.authentication.views.authentication_views.custom_404'
