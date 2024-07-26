from http import HTTPStatus

from asgiref.sync import sync_to_async

from django.views import View
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache

from apps.api.api_authentication.utils import token_handlers
from ..forms.form import LoginForm


__author__ = 'Ricardo'
__version__ = '0.1'


def custom_404(request, exception):
    return render(request, 'authentication/404.html', status=404)


class LoginView(View):

    form_class = LoginForm
    template_name = 'authentication/login.html'


    def get(self, request, *args, **kwargs):
        """
        This method return our login view
        """
        
        response = render(request, self.template_name, {'form':self.form_class,})
        return response
    

    def post(self, request, *args, **kwargs):
        """
        This method validates the login form.
        """
        form = self.form_class(request.POST)

        if not form.is_valid():
            return HttpResponse(content='Error, invalid form', status=HTTPStatus.BAD_REQUEST)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse(content='Error, user not found', status=HTTPStatus.NOT_FOUND)
        
        token = token_handlers.create_token(user)['access_token']
        callback_url = request.POST.get('redirect_uri')

        return JsonResponse(data={'callback_url':callback_url, 'code':token}, status=HTTPStatus.FOUND)
