from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from core.settings import CELERY_BROKER_URL
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CORE')

app.conf.broker_url = CELERY_BROKER_URL

app.autodiscover_tasks()

from celery.schedules import crontab
