from django.conf.urls.defaults import *

# place app url patterns here
urlpatterns = patterns('',
	url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/edit/(?P<path>[a-zA-Z0-9\-_\.\/]+)$', "commitlog.views.edit_file", name='commitlog-edit-file'),
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/tree/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', "commitlog.views.tree_view", name='commitlog-tree-view'),
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/$', "commitlog.views.log_view", name='commitlog-branch'),
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/$', "commitlog.views.branches_view", name='commitlog-branches'),
    url(r'^/$', "commitlog.views.repos_view", name='commitlog-repos'),
)