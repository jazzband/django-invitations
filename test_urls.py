from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    url(r'^invitations/', include(
        'invitations.urls', namespace='invitations')),
    url(r'^admin/', include(admin.site.urls)),
]

if 'allauth' in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r'^accounts/', include('allauth.urls'))
    )
