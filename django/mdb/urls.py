from django.conf.urls import patterns, include, url
from django.contrib import admin
from candidates import views
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^about-us/', views.AboutView.as_view(), name='about-us'),
    url(r'^elections2012/', views.Elections2012View.as_view(), name='elections2012'),
    url(r'^contact/', views.ContactView.as_view(), name='contact'),
    url(r'^admin/', include(admin.site.urls)),

    # api
    url(r'^api/candidates/', views.CandidateList.as_view()),
    url(r'^api/states/', views.StateList.as_view()),
    url(r'^api/job_roles/', views.JobRoleList.as_view()),
    url(r'^api/parties/', views.PartiesList.as_view()),

    #  candidates
    url(r'^candidates/political_party/$', views.PoliticalPartyListView.as_view(), name='political_party_list'),
    url(r'^candidates/list/(?P<type>\w+)/(?P<id>\d+)/$', views.CandidateListFilter.as_view(), name='candidates_list_filter'),
    url(r'^candidates/detail/(?P<candidate_id>[0-9]+)/$', views.CandidateDetail.as_view(), name='candidate_detail'),
    url(r'^candidates/search/', views.CandidateSearchView.as_view(), name='candidate_search'),
    url(r'^candidates/agendas/', views.AgendaListView.as_view(), name='agenda_list'),
    url(r'^candidates/agendas/(?P<agenda_id>[0-9]+)/$', views.AgendaCandidates.as_view(), name='agenda_candidates'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Change admin site title
admin.site.site_header = ("AppartidariAs - Admin")
