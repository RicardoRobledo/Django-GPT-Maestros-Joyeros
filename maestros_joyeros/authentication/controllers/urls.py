from django.urls import path
from django.contrib.auth.views import LogoutView

from maestros_joyeros.authentication.views import authentication_views


app_name = 'authentication_app'


urlpatterns = [
    path('login/', authentication_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
