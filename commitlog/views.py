# Create your views here.
from git import *
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from commitlog.settings import REPO_DIR, REPO_BRANCH, REPO_ITEMS_IN_PAGE, REPO_RESTRICT_VIEW

def log_view(request, page=0):
    repo = Repo(REPO_DIR)
    start = page + REPO_ITEMS_IN_PAGE
    commits = repo.iter_commits(REPO_BRANCH, max_count=start, skip=start + REPO_ITEMS_IN_PAGE)
    return TemplateResponse(request, 'commitlog/commitlog.html', {'commits': commits})

if REPO_RESTRICT_VIEW:
	log_view = login_required(log_view)