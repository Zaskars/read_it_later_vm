import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'read_it_later.settings')

app = Celery('read_it_later')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
