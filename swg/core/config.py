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
import datetime
import codecs
import os

class Config:
  __instance = None;

  version = '1.2.6'

  def __init__(self):
    self.now            = datetime.datetime.now()
    
    self.editor         = 'vim'
    self.datapath       = '.'
    self.dbpath         = os.path.join( self.datapath, 'db' )
    self.dbitem_ext     = "txt"
    self.hierarchy      = os.path.join( self.dbpath, 'categories.' + self.dbitem_ext )
    self.tplpath        = os.path.join( self.datapath, 'templates' )
    self.tplcache       = os.path.join( self.datapath, 'cache' )
    self.outputpath     = "output"
    self.copypaths      = {}

    self.siteurl        = ""
    self.sitename       = "Generated with SWG " + self.version
    self.charset        = "utf-8"
    self.language       = "en"
    self.keywords       = []
    
    self.basepath       = '/'
    self.page_ext       = "html"
    self.pager          = False
    self.items_per_page = 10

    self.gzip           = False
    self.compression    = 0
    self.tidyfy         = False
    
    self.transfer       = None

  def load( self, filename ):
    fd = codecs.open( filename, "r", "utf-8" )

    for line in iter(fd):
      line = line.strip()
      if line != '' and line[0] != '#':
        (key,value) = line.split( '=', 1 )
        key   = key.strip()
        value = value.strip()
        if key == 'dbitem_ext':
          self.dbitem_ext = value
        elif key == 'siteurl':
          self.siteurl = value 
        elif key == 'sitename':
          self.sitename = value
        elif key == 'charset':
          self.charset = value
        elif key == 'language':
          self.language = value
        elif key == 'basepath':
          self.basepath = value
        elif key == 'page_ext':
          self.page_ext = value
        elif key == 'editor':
          self.editor = value
        elif key == 'outputpath':
          self.outputpath = value
        elif key == 'pager':
          self.pager = True if value.lower() == 'true' else False
        elif key == 'gzip':
          self.gzip = True if value.lower() == 'true' else False
        elif key == 'tidyfy':
          self.tidyfy = True if value.lower() == 'true' else False
        elif key == 'compression':
          self.compression = int(value)
        elif key == 'items_per_page':
          self.items_per_page = int(value)
        elif key == 'copypaths':
          items = value.split(',')
          items = map( lambda s: s.strip(), items )
          for item in items:
            self.copypaths[ os.path.join( self.datapath, item ) ] = os.path.join( self.outputpath, item )
        elif key == 'keywords':
          items = value.split(',')
          self.keywords = map( lambda s: s.strip(), items )
        elif key == 'transfer':
          self.transfer = value
        else:
          raise Exception( "Unknown configuration key '%s'" % key )

    fd.close()

  @classmethod
  def getInstance(cls):
    if cls.__instance is None:
      cls.__instance = Config()
    return cls.__instance
