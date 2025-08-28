import os
from celery import Celery

#sets up default default setting module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

#sets up new celery application for our django project 
app = Celery('awd_main')