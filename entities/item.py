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
  SLUGIFY_SPLIT_REGEXP  = re.compile( r'[^\w]+' )
  PAGER_ENABLED_CLASSES = (
    'entities.category.Category',
    'entities.tag.Tag',
    'entities.author.Author'
  )

  def __init__( self, path, title, extension ):
    self.path        = path
    self.title       = title
    self.extension   = extension
    self.name        = self.__generate_name()
    self.url         = "%s/%s.%s" % (self.path,self.name,self.extension)
    self.hash_id     = hashlib.md5( self.url.encode( "utf-8" ) ).hexdigest()
    self.digest      = ""
    self.npages      = 1
    self.gzip        = Config.getInstance().gzip
    self.compression = Config.getInstance().compression
    self.gzip_allow  = re.compile( '^.+\.' + Config.getInstance().page_ext + '$', re.IGNORECASE )

  def __generate_name( self ):
      result = []
      for word in Item.SLUGIFY_SPLIT_REGEXP.split( self.title.lower() ):
          result.extend( word.split() )

      return '-'.join(result)

  def __save_contents( self, filename, contents ):
    if self.gzip is True and self.gzip_allow.match( filename ):
      import gzip
      import cStringIO

      fdio = cStringIO.StringIO()
      fd   = gzip.GzipFile( mode = 'wb',  fileobj = fdio, compresslevel = 9 )
      fd.write( contents )
      fd.close()

      filename = filename + u'.gz'
      contents = fdio.getvalue()

    fd = open( filename.encode('UTF-8'), "w+b" )
    fd.write( contents )
    fd.close()
   

  def create(self):  
    config = Config.getInstance()
    path   = config.outputpath + os.sep + self.path

    if not os.path.exists( path ):
      os.mkdir(path)

    if config.pager == True and self.title == 'index' or str(self.__class__) in Item.PAGER_ENABLED_CLASSES:     
      self.custom['pager'] = Pager( '%s.%s'     % (self.name, self.extension),
                                    '%s-%%d.%s' % (self.name, self.extension) )
                                    
      if hasattr( self, 'items' ):
        self.custom['pager'].setPages( self.items )
      else:
        self.custom['pager'].setPages( self.custom['pages'] )

      self.npages = self.custom['pager'].getTotalPages()
     
      for filename in self.custom['pager']:
        filename = os.path.join( path, filename )
        content  = self.render()

        self.digest = hashlib.md5( content ).hexdigest()

        DiffManager.getInstance().checkItem( filename, self.hash_id, self.digest )

        self.__save_contents( filename, content )
    else:
      filename = os.path.join( path, "%s.%s" % (self.name, self.extension) )
      content  = self.render()

      self.digest = hashlib.md5( content ).hexdigest()

      DiffManager.getInstance().checkItem( filename, self.hash_id, self.digest )

      self.__save_contents( filename, content )
