import git
import commitlog
from django.utils import simplejson
#import json

from django.template.response import TemplateResponse
from django.template.loader import render_to_string, get_template
from django.http import  HttpResponse

from commitlog.settings import PARTIAL_PREFIX

def git_to_dict( blob ):
    properties = ("abspath", "name", "mode",  "hexsha", "path", "size", "type",  ) #"mime_type",
    return dict([ ( prop, getattr( blob, prop ) )  for prop in properties])

# json helper
def to_json(python_object):

    if isinstance(python_object, (git.Blob, git.Tree) ):
        return git_to_dict( python_object )

    if isinstance(python_object, commitlog.forms.FileUploadForm ):
        return python_object.as_p()
    return None
    #raise TypeError(repr(python_object) + ' is not JSON serializable')

def partial_json_convert( template_name, context ):
    partial_prefix = "_"
    tmpl_dir = template_name.split("/")
        
    partial_template_path = "/".join( [ tmpl_dir[:-1][0], "%s%s" % (partial_prefix, tmpl_dir[-1:][0]) ] )
    try:
        partial = render_to_string( partial_template_path, context)
    except TemplateDoesNotExist:
        return TemplateResponse( 
            request,
            template_name,
            context)
    else:
        context["html"] = partial
    return context

    
def mix_response(request, template_name, context, json_convert=None):

    if request.is_ajax():
        
        if json_convert:
            response_dict = json_convert( template_name, context )
        else:
            response_dict = partial_json_convert( template_name, context )

        return HttpResponse(simplejson.dumps(response_dict, default=to_json), mimetype='application/javascript')

    else:
    	return TemplateResponse( 
            request, 
            template_name, 
            context)

def error_view(request, msg, code=None):
    return TemplateResponse( 
            request, 
            'commitlog/error.html', 
            { "msg":msg, })
            
def make_crumbs( path ):
    breadcrumbs = []
    bread = path.split("/")
    for crumb in range(0, len(bread)-1):
        breadcrumbs.append( (bread[crumb], "/".join(bread[:crumb+1]) ))
        
    #breadcrumbs.append( (bread[-1], "#") )
    return breadcrumbs

