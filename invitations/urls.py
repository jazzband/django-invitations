from django.urls import re_path

from . import views

app_name = "invitations"
urlpatterns = [
    re_path(r"^send-invite/$", views.SendInvite.as_view(), name="send-invite"),
    re_path(
        r"^send-json-invite/$",
        views.SendJSONInvite.as_view(),
        name="send-json-invite",
    ),
    re_path(
        r"^accept-invite/(?P<key>\w+)/?$",
        views.AcceptInvite.as_view(),
        name="accept-invite",
    ),
]
