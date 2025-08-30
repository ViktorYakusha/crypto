from __future__ import absolute_import, unicode_literals
import os
import time
from datetime import datetime

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_project.settings')

app = Celery('crypto_project')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
