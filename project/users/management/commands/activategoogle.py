# Script to insert social app credentials from json file into the database to use social login
# Usage: python manage.py activategoogle <path_to_json_file>
# https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/

from django.core.management.base import BaseCommand, CommandError
from allauth.socialaccount.models import SocialApp
import json
import os

class Command(BaseCommand):
    help = 'Inserts social app credentials from json file into the database to use social login'

    # take in path to json file as argument
    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Path to the json file containing the social app credentials')

    def handle(self, *args, **options):
        
        file_path = options['json_file_path']
        if not file_path:
            raise CommandError('Please specify the path to the JSON file')
        
        if not os.path.exists(file_path):
            raise CommandError('The specified file path does not exist or is incorrect')
        
        with open(file_path) as f:
            data = json.load(f)

        provider = 'google'
        name = 'CoHabitat-Google'
        client_id = data['web']['client_id']
        secret = data['web']['client_secret']

        if SocialApp.objects.filter(provider=provider).exists():
            self.stdout.write(self.style.WARNING('Social app credentials for Google already exist in the database'))
            return
        else:
            SocialApp.objects.create(provider=provider, name=name, client_id=client_id, secret=secret)
            self.stdout.write(self.style.SUCCESS('Successfully inserted social app credentials for Google into the database'))

