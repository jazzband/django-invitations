from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^invitations/', include(
        'invitations.urls', namespace='invitations')),
    url(r'^accounts/', include('allauth.urls')),
)
