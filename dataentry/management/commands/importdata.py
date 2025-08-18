from django.core.management.base import BaseCommand,CommandError
# from dataentry.models import Student
from django.apps import apps
import csv

class Command(BaseCommand):
    help = 'Import data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='location of the file')
        parser.add_argument('model_name', type=str, help='name of the model')

    def handle(self, *args, **kwargs):
        ## logic for the code
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue
        
        if not model:
            raise CommandError(f'Model {model_name} not found in any app')
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from file succesfully!'))