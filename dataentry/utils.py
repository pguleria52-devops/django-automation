from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os

def get_all_custom_models():
    default_models = ['LogEntry','Permission','Group','ContentType','Session','User','Upload']
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models  

def check_csv_errors(actual_file_path,model_name):
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label,model_name)
            break
        except LookupError:
            continue

    if not model:
        raise CommandError(f"model{model_name} not found in any app!")    
    
    model_fields = [field.name for  field in model._meta.fields if field.name != 'id']

    try:
        with open(actual_file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames


            if csv_header != model_fields:
                raise DataError(f"CSV file does not match with the {model_name} table fields")
    except Exception as e:
        raise e

    return model       

def send_email_notification(mail_subject,message,to_email, attachment = None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e    
    
def generate_csv_file(model_name):
    #generating timestamp for current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H")

        #define the csv file/path
        exported_dir = 'exported_data'
        file_name = f'exported_{model_name}_data_{timestamp}.csv'   
        file_path = os.path.join(settings.MEDIA_ROOT, exported_dir,file_name)
        print('file_path==>', file_path)
        return file_path