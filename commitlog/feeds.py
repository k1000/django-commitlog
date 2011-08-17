# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _

import settings
from views import get_commits

class RecentCommits(Feed):
    title = u"Observatorio Tecnológico" 
    link = "/pages/"
    description = u"últimas entradas del Observatorio Tecnológico"
    language = settings.PAGE_DEFAULT_LANGUAGE
    
    def items(self):
        return published_under(1)[:NR_ITEMS]

    def item_title(self, item):
        return item.title()

    def item_description(self, item):
        return item.get_content(self.language, 'intro')

    def items(self, obj):
        repo = get_repo( repo_name )
        return get_commits(repo, branch)