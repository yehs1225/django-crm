from django.core.management.base import BaseCommand
from csv import DictReader
from leads.models import Lead,UserProfile

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_name',type=str)
        parser.add_argument('organizor_email',type=str)

    def handle(self, *args,**options):
        file_name=options['file_name']
        organizor_email=options['organizor_email']
        organization = UserProfile.objects.get(user__email=organizor_email)

        with open(file_name,'r') as read_obj:
            csv_reader = DictReader(read_obj)
            for row in csv_reader:
                first_name = row['first_name']
                last_name = row['last_name']
                age = row['age']
                email = row['email']

                #TODO create the lead
                Lead.objects.create(
                    organization=organization,
                    first_name=first_name,
                    last_name=last_name,
                    age=age,
                    email=email,
                )
