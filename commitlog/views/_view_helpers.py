from django.template.response import TemplateResponse

def mix_response(request, template_name, context):
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

