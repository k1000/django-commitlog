from django.conf.urls.defaults import *

# place app url patterns here
urlpatterns = patterns('',
    

	url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/edit/(?P<path>[a-zA-Z0-9\-_\.\/]+)$',
		"commitlog.views.file.edit_file", name='commitlog-edit-file'),

	url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/new/(?P<path>[a-zA-Z0-9\-_\.\/]+)$', 
		"commitlog.views.file.new_file", name='commitlog-new-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/delete/(?P<path>[a-zA-Z0-9\-_\.\/\\]+)$', 
        "commitlog.views.file.delete_file", name='commitlog-delete-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/rename/(?P<file_path>[a-zA-Z0-9\-_\.\/\\]+)$', 
        "commitlog.views.file.rename_file", name='commitlog-rename-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/(?P<commit_sha>[a-z0-9\-_]+)/view/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
        "commitlog.views.file.view_file", name='commitlog-view-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/tree/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
    	"commitlog.views.tree.tree_view", name='commitlog-tree-view'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/(?P<commit_sha>[a-zA-Z0-9\-_\.\/]*)/tree/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
        "commitlog.views.tree.tree_view", name='commitlog-commit-tree-view'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/view/(?P<commit_sha>[a-zA-Z0-9\-_\.\/]*)$', 
        "commitlog.views.commit.commit_view", name='commitlog-commit-view'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/history/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
        "commitlog.views.commit.log_view", name='commitlog-history-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/diff/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
        "commitlog.views.commit.diff_view", name='commitlog-diff-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/$', 
    	"commitlog.views.commit.log_view", name='commitlog-branch'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/undo/$', 
        "commitlog.views.commit.undo_commit", name='commitlog-undo'),
    
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/search/$', 
        "commitlog.views.meta.search_view", name='commitlog-search'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/$', 
    	"commitlog.views.meta.branches_view", name='commitlog-branches'),
    
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/consol/$', 
        "commitlog.views.meta.consol_view", name='commitlog-consol'),

    url(r'^$', 
    	"commitlog.views.meta.repos_view", name='commitlog-repos'),
)