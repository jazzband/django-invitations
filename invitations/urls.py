from django.urls import path, re_path

from . import views

app_name = "invitations"
urlpatterns = [
    path("send-invite/", views.SendInvite.as_view(), name="send-invite"),
    path(
        "send-json-invite/",
        views.SendJSONInvite.as_view(),
        name="send-json-invite",
    ),
    re_path(
        r"^accept-invite/(?P<key>\w+)/?$",
        views.AcceptInvite.as_view(),
        name="accept-invite",
    ),
]
