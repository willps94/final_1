from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^post_create/$', PostCreateView.as_view(), name='post_create'),
    url(r'^post/$', PostListView.as_view(), name='post_list'),
    url(r'^question/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post_detail'),
)