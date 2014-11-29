from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',

    url(r'^send-invite/$', views.SendInvite.as_view(),
        name='send-invite'),

    url(r'^accept-invite/(?P<key>\w+)/$', views.AcceptInvite.as_view(),
        name='accept-invite'),
    
)
