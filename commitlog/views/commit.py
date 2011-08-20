from django.contrib import messages
from django.contrib.auth.decorators import login_required

from _view_helpers import mix_response
from _git_helpers import get_repo, get_commits, get_commit, get_diff

from commitlog.settings import REPO_BRANCH, REPO_RESTRICT_VIEW, REPO_ITEMS_IN_PAGE, GITTER_MEDIA_URL

def log(request, repo_name, branch=REPO_BRANCH, path=None):
    page = int(request.GET.get("page", 0))
    repo = get_repo( repo_name )
    if path:
        paths = [path]
    else:
        paths = []
    
    commits = get_commits(repo, branch, paths, page)
    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        repo_name = repo_name,
        branch_name = branch,
        commits = commits,
        next_page = page + 1,
        path = path,
    )
    if page > 0:
        context["previous_page"] = page-1

    return mix_response( 
        request, 
        'commitlog/commitlog.html', 
        context)

if REPO_RESTRICT_VIEW:
    log = login_required(log)


def view(request, repo_name, branch, commit_sha=None):
    """
    view diffs of affeted files in the commit
    """
    commit = diff = None
    repo = get_repo( repo_name )
    commit_list = get_commit( repo, commit_sha)
    if commit_list:
        commit = commit_list[0]
        diff = get_diff( repo, commit_list[1].hexsha, commit.hexsha,  )

    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        repo_name = repo_name,
        branch_name = branch,
        diff = diff,
        commit = commit,
    )
    return mix_response( 
        request, 
        'commitlog/commit.html', 
        context)

def undo(request, repo_name, branch_name):
    """
    undo last commit
    """
    repo = get_repo( repo_name )
    git = repo.git
    reset_result = git.reset( "--soft" "HEAD^" )
    messages.success(request, reset_result ) 
    return redirect('commitlog-commit-view', repo_name, branch_name  )

def diff(request, repo_name, branch, path, commits=[]):
    """
    view file diffs betwin given commits
    """
    pass