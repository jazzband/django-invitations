from django.urls import url, include
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    url(r'^invitations/', include('invitations.urls')),
    url(r'^admin/', admin.site.urls),
]

if 'allauth' in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r'^accounts/', include('allauth.urls'))
    )
