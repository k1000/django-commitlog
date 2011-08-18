import os
import codecs
from git import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import Http404

from commitlog.settings import REPOS, REPO_BRANCH, REPO_ITEMS_IN_PAGE, REPO_RESTRICT_VIEW, FILE_BLACK_LIST, GITTER_MEDIA_URL, EDITABLE_MIME_TYPES

from commitlog.forms import TextFileEditForm, FileEditForm, FileDeleteForm, FileUploadForm, RenameForm


MSG_COMMIT_ERROR = "There were problems with making commit"
MSG_COMMIT_SUCCESS = u"Commit has been executed. %s"
MSG_NO_FILE = "File hasn't been found."
MSG_NO_FILE_IN_TREE = "File haven't been found under current tree."
MSG_CANT_VIEW = "Can't view file."
MSG_NOT_ALLOWED = "You are not allowed to view/edit this file."
MSG_RENAME_ERROR = "There been an error during renaming the file %s to %s."
MSG_RENAME_SUCCESS = "File %s has been renamed to %s"


def file_type_from_mime(mime):
    types = {
        "text/x-python" : "python",
        "text/css" : "css",
        "text/html" : "xml",
        "aplication/javascript" : "javascript",
        "aplication/json" : "javascript",
    }
    if mime in types:
        return types[mime]
    else:
        return mime

def file_type_from_ext(ext):
    types = {
        ".py" : "python",
        ".css" : "css",
        ".html" : "xml",
        ".js" : "javascript",
    }
    if ext in types:
        return types[ext]
    else:
        return ext

def handle_uploaded_file( path, f):
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def write_file( file_path, file_source, mode="w"):
    f = codecs.open(file_path, encoding='utf-8', mode=mode)
    try:
        f.write(file_source)
    except IOError:
        return False
    finally:
        return True

def make_crumbs( path ):
    breadcrumbs = []
    bread = path.split("/")
    for crumb in range(0, len(bread)-1):
        breadcrumbs.append( (bread[crumb], "/".join(bread[:crumb+1]) ))
        
    #breadcrumbs.append( (bread[-1], "#") )
    return breadcrumbs

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

def error_view(request, msg, code=None):
    return TemplateResponse( 
            request, 
            'commitlog/error.html', 
            { "msg":msg, })

class NotAllowedToView(Exception):
    """You are not allowed to view/edit this file"""


def get_commits(repo, branch, paths=[], page=0):
    return repo.iter_commits(branch, paths, max_count=REPO_ITEMS_IN_PAGE, skip=page * REPO_ITEMS_IN_PAGE )


def log_view(request, repo_name, branch=REPO_BRANCH, path=None):
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

    return TemplateResponse( 
        request, 
        'commitlog/commitlog.html', 
        context)

if REPO_RESTRICT_VIEW:
    log_view = login_required(log_view)


@login_required
def tree_view(request, repo_name, branch=REPO_BRANCH, path=None, commit_sha=None ):
    
    repo = get_repo( repo_name )
    commit, tree = get_commit_tree(repo, commit_sha)

    if path:
        if path[-1:] == "/":
            path = path[:-1]
        tree = tree[path]
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = os.path.join( repo.working_dir, path, request.FILES["file_source"].name)
            handle_uploaded_file(file_path, request.FILES['file_source'])

            msg = "file %s uploaded" % file_path
            result_msg = mk_commit(repo, msg, file_path )
            messages.success(request, result_msg )
    else:
        form = FileUploadForm( )

    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        repo_name = repo_name,
        branch_name = branch,
        commit = commit,
        upload_form = form,
        tree = tree.list_traverse(depth = 1),
        breadcrumbs = None, #make_crumbs(path),
        dir_path = path.split("/"),
    )

    return TemplateResponse( 
        request, 
        'commitlog/view_tree.html', 
        context)


@login_required
def new_file(request, repo_name, branch=REPO_BRANCH, path=None ):
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
    return TemplateResponse( 
        request, 
        'commitlog/new_file.html', 
        context)

@login_required
def edit_file(request, repo_name, branch=REPO_BRANCH, path=None ):

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

    #import ipdb; ipdb.set_trace()
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
        
    return TemplateResponse( 
        request, 
        'commitlog/edit_file.html', 
        context)

def delete_file(request, repo_name, branch, path):
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
    return TemplateResponse( 
        request, 
        'commitlog/delete_file.html', 
        context)

def diff_view(request, repo_name, branch, path, commits=[]):
    """
    view file diffs betwin given commits
    """
    pass

def view_file(request, repo_name, branch, path, commit_sha=None,):
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

    return TemplateResponse( 
        request, 
        'commitlog/view_file.html', 
        context)

def commit_view(request, repo_name, branch, commit_sha=None):
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
    return TemplateResponse( 
        request, 
        'commitlog/commit.html', 
        context)
        
def branches_view(request, repo_name):
    pass


def rename_file(request, repo_name, branch_name, path):
    repo = get_repo( repo_name )

    tree = repo.tree()
    try:
        tree = tree[path]
    except KeyError:
        msg = MSG_NO_FILE_IN_TREE
        return error_view( request, msg)

    if request.method == "post":
        form = RenameForm( request.POST )
        if form.is_valid():
            git = repo.git
            new_name = form.cleaned_data["new_name"]
            try:
                os.rename(path, new_name)
            except IOError:
                msg = MSG_RENAME_ERROR % (path, new_name)
                return error_view( request, msg)
            else:
                git.mv( path, new_name )
                msg = MSG_RENAME_SUCCESS % (path, new_name)
                commit_result = git.commit("-m", """%s""" % msg)
                messages.success(request, commit_result ) 
                dir_path = "/".join( path.split("/")[:-1] )
                return redirect('commitlog-tree-view', repo_name, branch, dir_path  )
        else:
            msg = MSG_RENAME_ERROR
    else:
        form = RenameForm( )

    context = dict(
        GITTER_MEDIA_URL = GITTER_MEDIA_URL,
        breadcrumbs = make_crumbs(path),
        form = form,
        repo_name = repo_name,
        branch_name = branch,
        path = path,
    ) 
    return TemplateResponse( 
        request, 
        'commitlog/rename_file.html', 
        context)

def repos_view(request):
    context = {
        "repos":dict([ (repo_name, get_repo( repo_name )) for repo_name in REPOS]),
    }
    return TemplateResponse( 
        request, 
        'commitlog/list_repos.html', 
        context)

def undo_commit(request, repo_name, branch_name):
    """
    undo last commit
    """
    repo = get_repo( repo_name )
    git = repo.git
    reset_result = git.reset( "--soft" "HEAD^" )
    messages.success(request, reset_result ) 
    return redirect('commitlog-commit-view', repo_name, branch_name  )
