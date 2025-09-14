"""
WSGI config for asel project for production deployment.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set environment variable for production
os.environ.setdefault('DJANGO_ENVIRONMENT', 'production')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asel.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
