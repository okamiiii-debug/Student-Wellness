"""
WSGI config for wellness_app project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wellness_app.settings')

application = get_wsgi_application()

# Use this for WSGI servers
app = application
