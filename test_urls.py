from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^invitations/', include(
        'invitations.urls', namespace='invitations')),
    url(r'^admin/', include(admin.site.urls)),
)

if 'allauth' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^accounts/', include('allauth.urls'))
    )
