# -*- coding: utf-8 -*-
# This file is part of SWG (Static Website Generator).
#
# Copyright(c) 2010-2011 Simone Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
# http://www.backbox.org
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
from swg.entities.page        import Page
from swg.core.itemparser      import ItemParser
from swg.core.authormanager   import AuthorManager
from swg.core.categorymanager import CategoryManager
from swg.core.tagmanager      import TagManager

class PageParser(ItemParser):
  MANDATORY_FIELDS = {
    'date'       : 'datetime',
    'author'     : 'string',
    'categories' : 'array',
    'tags'       : 'array',
    'title'      : 'string'
  }
  
  def __init__(self):
    ItemParser.__init__(self)
        
  def parse( self, filename ):
    ItemParser.parse( self, PageParser.MANDATORY_FIELDS, filename )

    page = Page( self.info['title'] )

    author = AuthorManager.getInstance().get( self.info['author'] )
    author.items.append(page)
    
    categories = []
    for title in self.info['categories']:
      category = CategoryManager.getInstance().get(title)
      category.items.append(page)
      categories.append( category )

    tags = []
    for title in self.info['tags']:
      tag = TagManager.getInstance().get(title)
      tag.items.append(page)
      tags.append( tag )

    page.datetime   = self.info['date']
    page.author     = author
    page.categories = categories
    page.tags       = tags
    page.abstract   = self.abstract
    page.content    = self.body

    # reset the state
    ItemParser.__init__(self)

    return page
