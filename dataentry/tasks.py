from awd_main.celery import app
import time
from django.core.management import call_command
from .utils import send_email_notification
from django.conf import settings

@app.task
def celery_test_task():
    time.sleep(10)
    #send an email
    mail_subject = 'Test subject'
    message = 'This is a test email'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)
    return 'Email sent succesfully'

@app.task
def import_data_task(actual_file_path,model_name):
    try:
        call_command('importdata', actual_file_path, model_name)
        # messages.success(request, 'Data imported successfully')
    except Exception as e:
        raise e
    mail_subject = "Your mail subject imported successfully"
    message = "Your message has been imported"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)
    return 'Data imported succesfully'
        # messages.error(request, f'Error importing data: {str(e)}')
        # print(f"Import error: {e}")  # For debugging