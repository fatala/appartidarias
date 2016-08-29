from django.conf.urls import patterns, include, url
from django.contrib import admin
from candidates import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.hello),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/candidates/', views.CandidateList.as_view()),
)
