"""
WSGI config for ECommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application


PROJECT_DIR = Path(__file__).resolve().parents[1]
# Some hosts import this file from the repository root instead of beside manage.py.
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ECommerce.settings")

application = get_wsgi_application()
