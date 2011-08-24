
from django.contrib.auth.decorators import login_required

from _view_helpers import mix_response, make_crumbs
from _git_helpers import get_repo, get_commit_tree

from commitlog.forms import FileUploadForm
from commitlog.settings import  REPO_BRANCH, GITTER_MEDIA_URL

@login_required
def view(request, repo_name, branch=REPO_BRANCH, path=None, commit_sha=None ):
    
    repo = get_repo( repo_name )
    commit, tree = get_commit_tree(repo, commit_sha)
    dir_path = path.split("/")

    if path:
        if path[-1:] == "/":
            path = path[:-1]
        try:
            tree = tree[path]
        except AttributeError:
            tree = tree[dir_path[:-1]]
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = os.path.join( repo.working_dir, path, request.FILES["file_source"].name)
            handle_uploaded_file(file_path, request.FILES['file_source'])

            msg = "file %s uploaded" % file_path
            result_msg = mk_commit(repo, msg, file_path )
            messages.success(request, result_msg )
    else:
        form = FileUploadForm( initial={ "dir_path": path } )

    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        repo_name = repo_name,
        branch_name = branch,
        commit = commit,
        upload_form = form,
        tree = tree.list_traverse(depth = 1),
        breadcrumbs = make_crumbs(path),
        dir_path = dir_path,
    )

    return mix_response( 
        request, 
        'commitlog/view_tree.html', 
        context)