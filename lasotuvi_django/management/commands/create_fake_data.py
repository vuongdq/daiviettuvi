from django.core.management.base import BaseCommand
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from lasotuvi_django.fake_data import create_fake_data

class Command(BaseCommand):
    help = 'Creates fake data for the website'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating fake data...')
        create_fake_data()
        self.stdout.write(self.style.SUCCESS('Successfully created fake data')) 