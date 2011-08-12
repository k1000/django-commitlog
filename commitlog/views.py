# Create your views here.
import codecs
from git import *
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib import messages

from commitlog.settings import REPO_DIR, REPO_BRANCH, REPO_ITEMS_IN_PAGE, REPO_RESTRICT_VIEW, FILE_BLACK_LIST
from commitlog.forms import TextFileEditForm, FileEditForm

def log_view(request, branch=REPO_BRANCH):
    page = int(request.GET.get("page", 0))
    repo = Repo(REPO_DIR)
    #import ipdb; ipdb.set_trace()
    commits = repo.iter_commits(branch, max_count=REPO_ITEMS_IN_PAGE, skip=page * REPO_ITEMS_IN_PAGE )

    context = dict(
        branch_name = branch,
        commits = commits,
        next_page = page + 1,
    )
    if page > 0:
        context["previous_page"] = page-1

    return TemplateResponse( 
        request, 
        'commitlog/admin_commitlog.html', 
        context)

if REPO_RESTRICT_VIEW:
    log_view = login_required(log_view)





@login_required
def tree_view(request, branch=REPO_BRANCH, path=None ):

    repo = Repo(REPO_DIR)
    tree = repo.tree()
    if path:
        if path[-1:] == "/":
            path = path[:-1]
        tree = tree[path]

    context = dict(
        branch_name = branch,
        tree = tree.list_traverse(depth = 1),
        dir_path = path.split("/"),
    )

    return TemplateResponse( 
        request, 
        'commitlog/admin_view_tree.html', 
        context)

def guess_file_type(path):
    import os
    basename, extension = os.path.splitext(path)
    ext = {
        ".py" : {"type":"python", "mime":"text"},
        ".html" : {"type":"xml", "mime":"text"},
        ".css" : {"type":"css", "mime":"text"},
        ".js" : {"type":"javascript", "mime":"text"},
        ".json" : {"type":"javascript", "mime":"text"},
        ".svg" : {"type":"svg", "mime":"text"},
        ".txt" : {"type":"text", "mime":"text"},
        ".png" : {"type":"css", "mime":"image"},
        ".jpg" : {"type":"jpg", "mime":"image"},
        ".gif" : {"type":"gif", "mime":"image"},
        ".pdf" : {"type":"pdf", "mime":"doc"},
        ".doc" : {"type":"doc", "mime":"doc"},
    }
    if extension in ext:
        return ext[extension]
    else:
        return {"type":"text", "mime":"text"}

def handle_uploaded_file( path, f):
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def write_file( file_path, file_source):
    f = codecs.open(file_path, encoding='utf-8', mode='w')
    try:
        f.write(file_source)
    except Exception, e:
        raise
    finally:
        return True


@login_required
def edit_file(request, branch=REPO_BRANCH, path=None ):
    import os

    result_msg = ""
    file_source = ""
    repo = Repo(REPO_DIR)

    if path in FILE_BLACK_LIST:
        pass
    
    tree = repo.tree()
    if path[-1:] == "/":
        path = path[:-1]
    tree = tree[path]

    file_path = tree.abspath

    file_mime = tree.mime_type
    file_mime_type = file_mime.split("/")[0]

    file_type = guess_file_type(path)

    if file_mime_type == "text":
        form_class = TextFileEditForm
    else:
        form_class = FileEditForm
    
    if request.method == 'POST':
        form = form_class( request.POST, request.FILES )

        if form.is_valid():
            #f = open(file_path, "rw")
            if file_mime_type == "text":
                file_source = form.cleaned_data["file_source"]
                write_file(file_path, file_source )
            else:
                handle_uploaded_file(file_path, request.FILES['file_source'])

            index = repo.index
            message = form.cleaned_data["message"]
            try:
                #git = repo.git
                #commit_result = git.commit("-m", """%s""" % message)
                
                commit_result = index.commit("""%s""" % message)
            except GitCommandError as er:
                result_msg = u"There been problem applying you commit. %s" % er
                raise
            else:
                result_msg = u"Commit has been executed. <br/>%s" % commit_result
        else:
            result_msg = "There were problems with making commit"

    else:
        
        if file_mime_type == "text":
            f = codecs.open(file_path, encoding='utf-8',)
            file_source = f.read
        else:
            file_source = file_path

        form = form_class( initial={"file_source":file_source} )

    context = dict(
        form= form,
        file_source = file_source,
        file_type = file_type,
        result_msg = result_msg,
        branch_name = branch,
        dir_path = path.split("/")[:-1],
        path = path,
    )
        
    return TemplateResponse( 
        request, 
        'commitlog/admin_edit_file.html', 
        context)