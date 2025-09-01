import os
from celery import Celery

#sets up default default setting module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awd_main.settings')

#sets up new celery application for our django project 
app = Celery('awd_main')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')