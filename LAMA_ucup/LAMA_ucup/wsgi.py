"""
WSGI config for LAMA_ucup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from .kafka.consumer import Listener

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LAMA_ucup.settings')

application = get_wsgi_application()

# listener = Listener()
# listener.start()