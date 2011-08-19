from django.utils import simplejson
from django.template.response import TemplateResponse
from django.template.loader import render_to_string, get_template
from django.http import  HttpResponse

from commitlog.settings import PARTIAL_PREFIX

def mix_response(request, template_name, context, partial_prefix = "_"):

    if request.is_ajax():
        tmpl_dir = template_name.split("/")
        
        partial_template_path = "/".join( [ tmpl_dir[:-1][0], "%s%s" % (partial_prefix, tmpl_dir[-1:][0]) ] )
        try:
            rendered = render_to_string( partial_template_path, context)
        except TemplateDoesNotExist:
            return TemplateResponse( 
                request, 
                template_name, 
                context)
        else:
            return HttpResponse(rendered, mimetype='application/javascript')

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

