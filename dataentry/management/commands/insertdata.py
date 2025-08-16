from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    help = 'It will insert data into the database'

    def handle(self, *args, **kwargs):
        dataset = [
            {'roll_no': 12, 'name': 'Parimal', 'age': 26},
            {'roll_no': 10, 'name': 'Arsalan', 'age': 21},
            {'roll_no': 15, 'name': 'Pavan', 'age': 23},
            {'name': 'Raju', 'roll_no': 89, 'age': 26},
            {'name': 'Partikshit', 'roll_no': 25, 'age': 25},
            {'name': 'Shashank', 'roll_no': 54, 'age': 26},
        ]
        for data in dataset:
            # print(data['name'])
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()

            if not existing_record:
                Student.objects.create(name = data['name'], roll_no = data['roll_no'], age = data['age'])
            else:
                self.stdout.write(self.style.WARNING(f'The particular {roll_no} already exists.'))    
        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))