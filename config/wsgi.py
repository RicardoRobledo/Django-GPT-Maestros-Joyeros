"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')


def startup():
    """
    This method initialize services
    """

    print('Configuring services...')
    print('Configuring matplotlib...')

    # Configure matplotlib to work without server
    import matplotlib
    matplotlib.use('Agg')

    print('matplotlib configured!')


startup()
application = get_wsgi_application()
