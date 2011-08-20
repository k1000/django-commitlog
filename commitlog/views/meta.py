from commitlog.settings import REPOS, REPO_BRANCH, GITTER_MEDIA_URL
from commitlog.forms import SearchForm

from _view_helpers import mix_response
from _git_helpers import get_repo

def repos(request):
    context = {
        "repos":dict([ (repo_name, get_repo( repo_name )) for repo_name in REPOS]),
    }
    return mix_response( 
        request, 
        'commitlog/list_repos.html', 
        context)

def branches(request, repo_name):
    pass
          
def search(request, repo_name, branch):
    """
    serch files for string
    """
    found_files = []
    query = ""
    repo = get_repo( repo_name )
    if request.method == 'POST':
        form = SearchForm( request.POST )
        query = request.POST.get("query", "")
        if query:
            git = repo.git
            #http://book.git-scm.com/4_finding_with_git_grep.html
            try:
                result = git.grep( "--name-only", query )
            except GitCommandError:
                pass
            else:
                found_files = result.split("\n")
    else:
        form = SearchForm( request.POST )
    
    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        form = form,
        query = query,
        found_files = found_files,
        repo_name = repo_name,
        branch_name = branch,
    ) 

    return mix_response( 
        request, 
        'commitlog/found_files.html', 
        context)

def consol(request, repo_name):
    """
    serch files for string
    """
    result = ""
    query = ""
    repo = get_repo( repo_name )
    if request.method == 'POST':
        query = request.POST.get("console-input", "")
        if query:
            git = repo.git
            #http://book.git-scm.com/4_finding_with_git_grep.html
            result = git.grep( "--name-only", query )
            
        
    return HttpResponse(result, mimetype='application/javascript')