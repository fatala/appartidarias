from django.contrib import admin
from candidates.models import Candidate, PoliticalParty, Agenda


admin.site.register(Candidate)
admin.site.register(PoliticalParty)
admin.site.register(Agenda)
