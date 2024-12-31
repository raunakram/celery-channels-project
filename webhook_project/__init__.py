from __future__ import absolute_import, unicode_literals

# Import Celery app so it is loaded when Django starts
from .celery import app as celery_app

__all__ = ['celery_app']
