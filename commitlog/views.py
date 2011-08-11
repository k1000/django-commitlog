# Create your views here.
from git import *
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib import messages

from commitlog.settings import REPO_DIR, REPO_BRANCH, REPO_ITEMS_IN_PAGE, REPO_RESTRICT_VIEW
from commitlog.forms import FileEditForm

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

def edit_file(request, branch=REPO_BRANCH, path=None ):
    import os
    import codecs

    result_msg = ""
    file_source = ""
    repo = Repo(REPO_DIR)

    file_path = os.path.join( repo.working_dir, path ) #!!! sanitize path
    
    if request.method == 'POST':
        
        form = FileEditForm( request.POST )
        if form.is_valid():
            #f = open(file_path, "rw")
            f = codecs.open(file_path, encoding='utf-8', mode='w')
            file_source = form.cleaned_data["file_source"]
            try:
                f.write(file_source)
            except Exception, e:
                raise
            finally:
                message = form.cleaned_data["message"]
                git = repo.git
                commit_result = git.commit("-am", """%s""" % message)
                result_msg = u"Commit has een executed. %s" % commit_result
        else:
            result_msg = "There were problems with making commit"

    else:
        f = codecs.open(file_path, encoding='utf-8',)
        file_source = f.read

        form = FileEditForm( initial={"file_source":file_source} )
    #
    context = dict(
        form= form,
        file_source = file_source,
        result_msg = result_msg,
        branch_name = branch,
        path = path,
    )
        
    return TemplateResponse( 
        request, 
        'commitlog/admin_edit_file.html', 
        context)