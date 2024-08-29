from celery import Celery
import enum
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python.io_atomgroup.soccer.settings')

app = Celery('python.io_atomgroup.soccer')

import django.conf

class Queue(enum.Enum):
    celery = 'celery'
    admin = 'admin'


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = django.conf.settings.CELERY_BROKER_URL

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.autodiscover_tasks([
    'python.io_atomgroup.soccer.estimator',
])
