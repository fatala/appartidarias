from django.core.management.base import BaseCommand
from candidates.models import Candidate, PoliticalParty, JobRole

class Command(BaseCommand):
    def handle(self, *args, **options):
        Candidate.objects.all().delete()
        PoliticalParty.objects.all().delete()
        JobRole.objects.all().delete()