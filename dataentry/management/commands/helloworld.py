from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Prints the hello world'

    def handle(self, *args, **kwargs):
        self.stdout.write("Hello World")