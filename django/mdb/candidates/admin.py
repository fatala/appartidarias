from django.contrib import admin
from candidates.models import (
    Agenda, Candidate, Comment, JobRole, PoliticalParty, Contact
)
from django.utils.safestring import mark_safe


class PoliticalPartyAdmin(admin.ModelAdmin):
    list_display = ('number', 'initials', 'name')
    readonly_fields = ('ranking', 'size', 'women_pct', 'money_women_pct')


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name_ballot', 'political_party', 'number', 'job_role')
    search_fields = ('name_ballot', 'number')
    list_filter = ('political_party', 'job_role')

    readonly_fields = ('picture',)

    def picture(self, instance):
        result = u'<img src=%s/>' % instance.picture_url
        return mark_safe(result)
    picture.short_description = "Foto do candidato"


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'candidate', 'approved',
    )

    raw_id_fields = (
        'candidate',
    )
    list_filter = ('approved', )
    readonly_fields = ('created_at',)


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'created_at', 'reviewed',
    )

    list_filter = ('reviewed', )
    readonly_fields = ('created_at',)

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(PoliticalParty, PoliticalPartyAdmin)
admin.site.register(Agenda)
admin.site.register(JobRole)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contact, ContactAdmin)
