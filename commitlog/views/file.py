
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from _view_helpers import mix_response, make_crumbs
from _git_helpers import get_repo, get_commit_tree, get_diff
from _os_helpers import file_type_from_mime

from commitlog.settings import REPOS, REPO_BRANCH, REPO_ITEMS_IN_PAGE, REPO_RESTRICT_VIEW
from commitlog.settings import FILE_BLACK_LIST, GITTER_MEDIA_URL, EDITABLE_MIME_TYPES

from commitlog.forms import TextFileEditForm, FileEditForm, FileDeleteForm, FileUploadForm, RenameForm, SearchForm

MSG_COMMIT_ERROR = "There were problems with making commit"
MSG_COMMIT_SUCCESS = u"Commit has been executed. %s"
MSG_NO_FILE = "File hasn't been found."
MSG_NO_FILE_IN_TREE = "File haven't been found under current tree."
MSG_CANT_VIEW = "Can't view file."
MSG_NOT_ALLOWED = "You are not allowed to view/edit this file."
MSG_RENAME_ERROR = "There been an error during renaming the file %s to %s."
MSG_RENAME_SUCCESS = "File %s has been renamed to %s"

@login_required
def new(request, repo_name, branch=REPO_BRANCH, path=None ):
    result_msg = file_source = ""
    form_class = TextFileEditForm

    file_path = path #!!! FIX security
    #TODO check if file exist allready
    file_meta = dict(
        type = "python",
    )

    if request.method == 'POST':
        form = form_class( request.POST, request.FILES )
        if form.is_valid():
            repo = Repo(REPOS[repo_name])

            file_source = form.cleaned_data["file_source"]
            write_file(file_path, file_source )

            msg = form.cleaned_data["message"]
            result_msg = mk_commit(repo, msg, file_path )
            messages.success(request, result_msg ) 

            dr_path = "/".join( path.split("/")[:-1] )
            return redirect('commitlog-tree-view', repo_name, branch, dir_path  )
        else:
            result_msg = MSG_COMMIT_ERROR
    else:
        form = form_class( initial={"message":"%s added" % path} )
    
    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        form= form,
        breadcrumbs = make_crumbs(path),
        result_msg = result_msg,
        file_meta = file_meta,
        repo_name = repo_name,
        branch_name = branch,
        path = path,
    )
    return mix_response( 
        request, 
        'commitlog/new_file.html', 
        context)



@login_required
def edit(request, repo_name, branch=REPO_BRANCH, path=None ):

    result_msg = file_source = ""

    if path in FILE_BLACK_LIST:
        msg = MSG_NOT_ALLOWED
        return error_view( request, result_msg)
    
    if path[-1:] == "/":
        path = path[:-1]
    file_path = path #!!! FIX security

    repo = get_repo( repo_name )
    tree = repo.tree()
    
    try:
        tree = tree[path]
    except KeyError:
        msg = MSG_NO_FILE_IN_TREE
        return error_view( request, msg)

    if not tree.type  is "blob":
        msg = MSG_CANT_VIEW
        return error_view( request, msg)
    
    mime = tree.mime_type.split("/")
    file_meta = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        abspath = tree.abspath,
        mime = tree.mime_type,
        size = tree.size,
        tree = tree,
        mime_type = mime[0],
        type = file_type_from_mime(tree.mime_type),
    )

    if file_meta["mime_type"] in EDITABLE_MIME_TYPES:
        form_class = TextFileEditForm
    else:
        form_class = FileEditForm
    
    if request.method == 'POST':
        
        form = form_class( request.POST, request.FILES )
        if form.is_valid():
            if file_meta["mime_type"] == "text":
                file_source = form.cleaned_data["file_source"]
                write_file(file_path, file_source )
            else:
                handle_uploaded_file(file_path, request.FILES['file_source'])

            message = form.cleaned_data["message"]
            result_msg = mk_commit(repo, message, file_path )
        else:
            result_msg = MSG_COMMIT_ERROR
    else:
        if file_meta["mime_type"] in EDITABLE_MIME_TYPES:
            file_source = tree.data_stream[3].read
        else:
            file_source = file_meta["abspath"]

        form = form_class( initial={
            "file_source":file_source,
            "message":"modified %s" % path
        } )

    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        form= form,
        file_source = file_source,
        breadcrumbs = make_crumbs(path),
        file_meta = file_meta,
        result_msg = result_msg,
        repo_name = repo_name,
        branch_name = branch,
        path = path,
    )
        
    return mix_response( 
        request, 
        'commitlog/edit.html', 
        context)


def view(request, repo_name, branch, path, commit_sha=None,):
    """
    view file in the commit
    """
    file_source = diff = ""

    if path in FILE_BLACK_LIST:
        msg = MSG_NOT_ALLOWED
        return error_view( request, msg)
    
    file_path = path #!!! FIX security
    if path[-1:] == "/": path = path[:-1]
    
    repo = get_repo( repo_name )
    commit, tree = get_commit_tree( repo, commit_sha )

    if commit.parents:
        diff = get_diff( repo, path, commit.parents[0].hexsha, commit.hexsha )

    try:
        tree = tree[path]
    except KeyError:
        msg = MSG_NO_FILE_IN_TREE
        return error_view( request, msg )

    if not tree.type  is "blob":
        msg = MSG_NO_FILE_IN_TREE
        return error_view( request, msg )
    
    mime = tree.mime_type.split("/")
    
    file_source = tree.data_stream[3].read()
    
    #import ipdb; ipdb.set_trace()
    file_meta = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        abspath = tree.abspath,
        mime = tree.mime_type,
        size = tree.size,
        tree = tree,
        path = tree.abspath,
        mime_type = mime[0],
        type = file_type_from_mime(tree.mime_type),
    )
    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        file_source = file_source,
        breadcrumbs = make_crumbs(path),
        commit = commit,
        diff = diff,
        file_meta = file_meta,
        repo_name = repo_name,
        branch_name = branch,
        path = path,
    )
    if mime[0] == "image":
        import base64
        context["img_base"] = base64.b64encode( file_source )

    return mix_response( 
        request, 
        'commitlog/view_file.html', 
        context)

def delete(request, repo_name, branch, path):
    repo = get_repo( repo_name )
    tree = repo.tree()
    try:
        ftree = tree[path] #check if exixs under the tree
    except KeyError:
        pass

    if request.method == "POST":
        form = FileDeleteForm(request.POST)
        if form.is_valid():
            if os.path.isfile(path):
                os.remove(path)
            git = repo.git
            del_message = git.rm(path)

            msg = form.cleaned_data["message"]
            commit_result = git.commit("-m", """%s""" % msg)
            messages.success(request, commit_result ) 

            dir_path = "/".join( path.split("/")[:-1] )
            return redirect('commitlog-tree-view', repo_name, branch, dir_path  )
    else:
        form = FileDeleteForm(initial={
            "message": "file %s deleted" % path,
            "path": path,
        })
    
    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        breadcrumbs = make_crumbs(path),
        form = form,
        repo_name = repo_name,
        branch_name = branch,
        path = path,
    )
    return mix_response( 
        request, 
        'commitlog/delete_file.html', 
        context)

def rename(request, repo_name, branch, file_path):

    if request.method == 'POST':
        repo = get_repo( repo_name )
        tree = repo.tree()
        try:
            tree = tree[file_path]
        except KeyError:
            msg = MSG_NO_FILE_IN_TREE
            return error_view( request, msg)

        form = RenameForm( request.POST )
        
        if form.is_valid():

            git = repo.git
            new_name = form.cleaned_data["new_name"]
            try:
                os.rename(file_path, new_name)
            except IOError:
                msg = MSG_RENAME_ERROR % (file_path, new_name)
                return error_view( request, msg)
            else:
                
                git.mv( path, new_name )
                msg = MSG_RENAME_SUCCESS % (path, new_name)
                commit_result = git.commit("-m", """%s""" % msg)
                messages.success(request, commit_result ) 
                dir_path = "/".join( path.split("/")[:-1] )
                return redirect('commitlog-tree-view', repo_name, branch, dir_path  )
        else:
            messages.error(request, MSG_RENAME_ERROR ) 
    else:
        form = RenameForm( )

    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        breadcrumbs = make_crumbs(file_path),
        form = form,
        repo_name = repo_name,
        branch_name = branch,
        path = file_path,
    ) 
    return mix_response( 
        request, 
        'commitlog/rename_file.html', 
        context)