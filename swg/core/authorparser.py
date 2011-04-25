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
from swg.core.itemparser import ItemParser
from swg.entities.author import Author

class AuthorParser(ItemParser):
  MANDATORY_FIELDS = {
    'username' : 'string',
    'avatar'   : 'string',
    'email'    : 'string',
    'website'  : 'string'
  }

  def __init__(self):
    ItemParser.__init__(self)

  def parse( self, filename ):
    ItemParser.parse( self, AuthorParser.MANDATORY_FIELDS, filename )
    
    object = Author( self.info['username'] )
    object.avatar   = self.info['avatar']
    object.email    = self.info['email']
    object.website  = self.info['website']
    object.content  = self.body
    object.abstract = self.abstract

    return object
