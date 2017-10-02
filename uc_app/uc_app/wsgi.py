"""
WSGI config for uc_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/cs4501/app/uc_app')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uc_app.settings")

application = get_wsgi_application()
