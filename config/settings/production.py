from .base import *


DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'django-gpt-maestros-joyeros.onrender.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
