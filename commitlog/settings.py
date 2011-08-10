# Create your views here.
  
from django.conf import settings

REPO_DIR = getattr(settings, "REPO_DIR", "")
REPO_BRANCH = getattr(settings, "REPO_BRANCH", "master")
