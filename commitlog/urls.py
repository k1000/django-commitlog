from django.conf.urls.defaults import *

# place app url patterns here
urlpatterns = patterns('',
	url(r'^(?P<branch>[a-z0-9\-_]+)/edit/(?P<path>[a-z0-9\-_\.\/]+)$', "commitlog.views.edit_file", name='commitlog-edit-file'),
    url(r'^(?P<branch>[a-z0-9\-_]+)/tree/(?P<path>[a-z0-9\-_\.\/]*)$', "commitlog.views.tree_view", name='commitlog-tree-view'),
    url(r'^(?P<branch>[a-z0-9\-_]+)/$', "commitlog.views.log_view", name='commitlog-branch'),
)