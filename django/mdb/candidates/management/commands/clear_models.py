from django.core.management.base import BaseCommand
from candidates.models import Candidate, PoliticalParty

class Command(BaseCommand):
    def handle(self, *args, **options):
        Candidate.objects.all().delete()