from git import *
from django.http import Http404
from commitlog.views._view_helpers import error_view
from commitlog.settings import REPOS, REPO_ITEMS_IN_PAGE

def mk_commit(repo, message, path ):
    git = repo.git
    #index = repo.index 
    try:
        git.add(path)    
        commit_result = git.commit("-m", """%s""" % message)
        #commit_result = index.commit("""%s""" % message)
    except GitCommandError:
        result_msg = MSG_COMMIT_ERROR
    else:
        result_msg = MSG_COMMIT_SUCCESS % commit_result
    return result_msg

def get_commit( repo, commit_sha ):
    return list(repo.iter_commits( rev = commit_sha ))

def get_repo( repo_name ):
    try:
        return Repo(REPOS[repo_name])
    except InvalidGitRepositoryError:
        raise Http404 
    except NoSuchPathError:
        raise Http404 #!!! FIXIT

def get_commit_tree( repo, commit_sha=None ):
    commit = None
    if commit_sha:
        commit = list(repo.iter_commits( rev=commit_sha ))[0]
        tree = commit.tree
    else:
        tree = repo.tree()
    return commit, tree

def get_diff(repo, path=None, commit_a=None, commit_b=None):
    git = repo.git
    args = []
    if commit_a: args+=[commit_a]
    if commit_b: args+=[commit_b]
    if path: args +=[ "--", path ]
    return git.diff( *args )

def get_commits(repo, branch, paths=[], page=0):
    return repo.iter_commits(branch, paths, max_count=REPO_ITEMS_IN_PAGE, skip=page * REPO_ITEMS_IN_PAGE )