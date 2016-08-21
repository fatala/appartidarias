from django.contrib import admin
from candidates.models import Candidate, PoliticalParty, Agenda, JobRole
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join

class CandidateAdmin(admin.ModelAdmin):
    readonly_fields = ('picture',)

    def picture(self, instance):
        result = '<img src=%s/>' % instance.picture_url
        return mark_safe(result)

    picture.short_description = "Foto do candidato"

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(PoliticalParty)
admin.site.register(Agenda)
admin.site.register(JobRole)