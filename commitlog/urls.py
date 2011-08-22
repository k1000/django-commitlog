from django.conf.urls.defaults import *

# place app url patterns here
urlpatterns = patterns('commitlog.views.file',
	url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/edit/(?P<path>[a-zA-Z0-9\-_\.\/]+)$',
		"edit", name='commitlog-edit-file'),

	url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/new/(?P<path>[a-zA-Z0-9\-_\.\/]+)$', 
		"new", name='commitlog-new-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/upload/', 
        "upload", name='commitlog-upload-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/delete/(?P<path>[a-zA-Z0-9\-_\.\/\\]+)$', 
        "delete", name='commitlog-delete-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/rename/(?P<file_path>[a-zA-Z0-9\-_\.\/\\]+)$', 
        "rename", name='commitlog-rename-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/(?P<commit_sha>[a-z0-9\-_]+)/view/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
        "view", name='commitlog-view-file'),
)

urlpatterns += patterns('commitlog.views.tree',
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/tree/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
    	"view", name='commitlog-tree-view'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/(?P<commit_sha>[a-zA-Z0-9\-_\.\/]*)/tree/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
        "view", name='commitlog-commit-tree-view'),
)

urlpatterns += patterns('commitlog.views.commit',
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/view/(?P<commit_sha>[a-zA-Z0-9\-_\.\/]*)$', 
        "view", name='commitlog-commit-view'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/history/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
        "log", name='commitlog-history-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/diff/(?P<path>[a-zA-Z0-9\-_\.\/]*)$', 
        "diff", name='commitlog-diff-file'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/$', 
    	"log", name='commitlog-log'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/undo/$', 
        "undo", name='commitlog-undo'),
)

urlpatterns += patterns('commitlog.views.meta',   
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/(?P<branch>[a-z0-9\-_]+)/search/$', 
        "search", name='commitlog-search'),

    url(r'^(?P<repo_name>[a-z0-9\-_]+)/$', 
    	"branches", name='commitlog-branches'),
    
    url(r'^(?P<repo_name>[a-z0-9\-_]+)/consol/$', 
        "consol", name='commitlog-consol'),

    url(r'^$', 
    	"repos", name='commitlog-repos'),
)