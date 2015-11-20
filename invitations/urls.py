from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',

    url(r'^send-invite/$', views.SendInvite.as_view(),
        name='send-invite'),

    url(r'^send-json-invite/$', views.SendJSONInvite.as_view(),
        name='send-json-invite'),

    url(r'^accept-invite/(?P<key>\w+)/?$', views.AcceptInvite.as_view(),
        name='accept-invite'),
)
