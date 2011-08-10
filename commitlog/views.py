# Create your views here.
from git import *

from django.template.response import TemplateResponse

from commitlog.settings import REPO_DIR, REPO_BRANCH, REPO_ITEMS_IN_PAGE

def log_view(request, page=0):
    repo = Repo(REPO_DIR)
    commits = repo.iter_commits(REPO_BRANCH, max_count=1010, skip=REPO_ITEMS_IN_PAGE)
    return TemplateResponse(request, 'commitlog/commitlog.html', {'commits': commits})
