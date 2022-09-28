from django.conf import settings
from django.contrib import admin
from django.urls import include, path

admin.autodiscover()

urlpatterns = [
    path("invitations/", include("invitations.urls")),
    path("admin/", admin.site.urls),
]

if "allauth" in settings.INSTALLED_APPS:
    urlpatterns.append(path("accounts/", include("allauth.urls")))
