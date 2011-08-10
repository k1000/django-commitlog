from django.conf.urls.defaults import *

# place app url patterns here
urlpatterns = patterns('commitlog.views',
    url(r'^(?P<branch>[-\w]+)/$', "log_view", name='commitlog-branch'),
    #url(r'^/$', login_required( LookingFormView.as_view() ), name='commitlog-branch'),
)