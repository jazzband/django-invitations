from django.conf.urls import patterns, url, include
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^invitations/', include(
        'invitations.urls', namespace='invitations')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
