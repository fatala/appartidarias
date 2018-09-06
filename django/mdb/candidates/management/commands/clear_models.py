from django.core.management.base import BaseCommand
from candidates.models import Candidate, PoliticalParty, JobRole, Expenses

class Command(BaseCommand):

    def handle(self, *args, **options):

        Candidate.objects.all().delete()
        JobRole.objects.all().delete()
        Expenses.objects.all().delete()
        Contact.objects.all().delete()
        Comment.objects.all().delete()
        PoliticalParty.objects.all().delete()
