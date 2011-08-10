# Create your views here.
  
from django.conf import settings

REPO_DIR = getattr(settings, "REPO_DIR", "")
REPO_BRANCH = getattr(settings, "REPO_BRANCH", "master")
REPO_RESTRICT_VIEW = getattr(settings, "REPO_RESTRICT_VIEW", True)
REPO_ITEMS_IN_PAGE = getattr(settings, "REPO_VIEW_IN_PAGE", 30)
 