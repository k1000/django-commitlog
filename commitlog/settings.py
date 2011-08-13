
from django.conf import settings

REPOS = getattr(settings, "REPOS", {
	"local":"",
})

REPO_BRANCH = getattr(settings, "REPO_BRANCH", "master")
REPO_RESTRICT_VIEW = getattr(settings, "REPO_RESTRICT_VIEW", True)
REPO_ITEMS_IN_PAGE = getattr(settings, "REPO_VIEW_IN_PAGE", 10)
FILE_BLACK_LIST = getattr(settings,"FILE_BLACK_LIST", 
	("settings.py",) 
)
GITTER_MEDIA_URL = getattr(settings,"GITTER_MEDIA_URL", settings.MEDIA_URL ) 
