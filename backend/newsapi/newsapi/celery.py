# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from decouple import config
from django.apps import apps
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','newsapi.settings')

BASE_REDIS_URL = config('REDIS_URL', default='redis://localhost:6379')
app = Celery('news')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = BASE_REDIS_URL

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

app.conf.beat_schedule = {
    'execute-every-even-hour': {
        'task': 'news.tasks.get_today_top_headlines',
        'schedule':crontab(minute=0, hour='*')
        # 'schedule': 20.0 # run for every 20 seconds
    },
}