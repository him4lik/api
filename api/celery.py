import os
from celery import Celery, Task
from . import settings
from celery.signals import after_setup_task_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')

app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.Task = Task

# @after_setup_task_logger.connect
# def on_celery_setup(**kwargs):
#     pass