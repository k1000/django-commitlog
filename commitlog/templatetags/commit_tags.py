# Create your views here.

#http://packages.python.org/GitPython/0.3.2/tutorial.html#obtaining-diff-information
#http://djangosnippets.org/snippets/944/
import datetime
from git import *
from django.template import Library, Node
from django.template.defaultfilters import stringfilter

from commitlog.settings import REPOS, REPO_BRANCH
register = Library()

class LatestCommitsNode(Node):
    def __init__(self, num, varname):
        self.num, self.varname = num, varname

    def render(self, context):
        repo = Repo(REPOS[repo_name])
        context[self.varname] = repo.iter_commits(REPO_BRANCH, max_count=self.num)
        return ''

@register.tag        
def get_recent_commits(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_recent_commits tag takes exactly three arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to get_recent_commits tag must be 'as'"
    return LatestCommitsNode(int(bits[1]), bits[3])


@register.filter
def mkdate(format_string):
    try:
        return datetime.datetime.fromtimestamp( float(format_string) )
    except ValueError:
        return format_string

@register.filter
def truncatechars(format_string, val):
    'Wed, 7 May 2008 05:56'
    #mport ipdb; ipdb.set_trace()
    return format_string[:val]

@register.simple_tag
def show_patch( diff ):
    return diff.diff

@register.simple_tag
def diff_parent( commit ):
    return commit.diff( commit.parents[0] )