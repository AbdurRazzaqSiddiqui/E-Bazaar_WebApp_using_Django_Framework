"""Expose the Django ASGI application to Vercel's Python runtime."""

from pathlib import Path
import os
import sys


PROJECT_DIR = Path(__file__).resolve().parents[1] / "ECommerce"
sys.path.insert(0, str(PROJECT_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ECommerce.settings")

from ECommerce.asgi import application  # noqa: E402


app = application
