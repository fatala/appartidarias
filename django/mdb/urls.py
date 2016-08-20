from django.conf.urls import patterns, include, url
from candidates import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^candidates/', views.CandidateList.as_view()),
)
