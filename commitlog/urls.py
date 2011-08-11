from django.conf.urls.defaults import *

# place app url patterns here
urlpatterns = patterns('',
    url(r'^(?P<branch>[a-z0-9\-_]+)/$', "commitlog.views.log_view", name='commitlog-branch'),
)