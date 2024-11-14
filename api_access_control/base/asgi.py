"""
ASGI config for base project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from decouple import config

if config('DEBUG', cast=bool):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.config.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.config.production')

application = get_asgi_application()
