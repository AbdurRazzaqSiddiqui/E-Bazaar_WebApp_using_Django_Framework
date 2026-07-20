"""
ASGI config for ECommerce project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application


PROJECT_DIR = Path(__file__).resolve().parents[1]
# Vercel imports this file from the repository root instead of beside manage.py.
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ECommerce.settings")

application = get_asgi_application()
