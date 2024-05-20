import os
from celery import Celery
from celery.schedules import crontab
from configurations import importer
from django.conf import settings
from environ import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LAMA_ucup.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

importer.install()

app = Celery("main", include=[
    "LAMA_ucup.integration_data.tasks"
])
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'task_product': {
        'task': 'task_product',
        'schedule': crontab(minute='*/5', hour='*')
    },
    'task_assort': {
        'task': 'task_assort',
        'schedule': crontab(minute='*/5', hour='*')
    },
    'task_vendor': {
        'task': 'task_vendor',
        'schedule': crontab(minute='*/5', hour='*')
    },
    'task_integration_store': {
        'task': 'task_integration_store',
        'schedule': crontab()  # float(env('CELERY_SCHEDULING_HIERARCHY'))
    },
}