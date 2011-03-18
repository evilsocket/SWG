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
import re
import os
import hashlib

from core.config      import Config
from core.diffmanager import DiffManager
from core.pager       import Pager

class Item:
  SLUGIFY_SPLIT_REGEXP  = re.compile( r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+' )
  PAGER_ENABLED_CLASSES = (
    'entities.category.Category',
    'entities.tag.Tag',
    'entities.author.Author'
  )

  def __init__( self, path, title, extension ):
    self.path      = path
    self.title     = title
    self.extension = extension
    self.name      = self.__generate_name()
    self.url       = "%s/%s.%s" % (self.path,self.name,self.extension)
    self.hash_id   = hashlib.md5( self.url.encode( "utf-8" ) ).hexdigest()
    self.digest    = ""
    self.npages    = 1

  def __generate_name( self ):
      result = []
      for word in Item.SLUGIFY_SPLIT_REGEXP.split( self.title.lower() ):
          result.extend( word.split() )

      return '-'.join(result)

  def create(self):  
    config = Config.getInstance()
    path   = config.outputpath + "/" + self.path

    if config.pager == True and self.title == 'index' or str(self.__class__) in Item.PAGER_ENABLED_CLASSES:     
      self.custom['pager'] = Pager( '%s.%s'     % (self.name, self.extension),
                                    '%s-%%d.%s' % (self.name, self.extension) )
                                    
      if hasattr( self, 'items' ):
        self.custom['pager'].setPages( self.items )
      else:
        self.custom['pager'].setPages( self.custom['pages'] )

      self.npages = self.custom['pager'].getTotalPages()
     
      for filename in self.custom['pager']:
        filename = ("%s/%s" % ( path, filename )).replace( '//', '/' )
        if not os.path.exists( path ):
          os.mkdir(path)

        content = self.render()

        self.digest = hashlib.md5( content ).hexdigest()

        DiffManager.getInstance().checkItem( filename, self.hash_id, self.digest )

        fd = open( filename, "w+" )
        fd.write(content)
        fd.close()
    else:
      filename = ("%s/%s.%s" % ( path, self.name, self.extension )).replace( '//', '/' )
      if not os.path.exists( path ):
        os.mkdir(path)

      content = self.render()

      self.digest = hashlib.md5( content ).hexdigest()

      DiffManager.getInstance().checkItem( filename, self.hash_id, self.digest )

      fd = open( filename, "w+" )
      fd.write(content)
      fd.close()