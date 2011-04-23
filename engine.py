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

import os
import sys
import os.path
import re
import shutil

from optparse         import OptionParser
from core.config      import Config
from core.pageparser  import PageParser
from entities.page    import Page
from core.diffmanager import DiffManager

class Engine:
  def __init__(self):
    self.config = Config.getInstance()
    self.dbdir  = os.path.join( self.config.dbpath, 'pages' )
    self.files  = os.listdir( dbdir ) 

  def new( self ):
    maxid = 0
    for file in self.files:
      ( id, ext ) = file.split('.')
      if int(id) > maxid:
        maxid = int(id)
    
    newitem = os.path.join( self.dbdir, "%d.%s" % (maxid + 1, self.config.dbitem_ext) )
    fd      = open( newitem, 'w+t' )

    fd.write(
"""Date: %s
Author:
Categories:
Tags:
Title:

""" % self.config.now.strftime("%Y-%m-%d %H:%M:%S") )

    fd.close()
    
    os.system( "%s %s" % ( self.config.editor, newitem ) )

    if os.path.exists( newitem ):
      print "@ Item '%s' created, you can now regenerate the website ." % newitem
    else:
      print "@ Item was not saved, quitting ."

  def serve( self ):
    pass

  def generate( self ):
    parser = PageParser( )
    pages  = []

    print "@ Parsing pages ..."
    for file in self.files:
      if re.match( '^.+\.' + self.config.dbitem_ext + '$', file ):
        filename = os.join( self.dbdir, file )
        page     = parser.parse( filename )
        pages.append(page)

    print "@ Sorting pages by date ..."
    pages.sort( reverse=True, key=lambda p: p.datetime )

    # delete output directory and recreate it
    if os.path.exists(self.config.outputpath ):
      print "@ Removing old '%s' path ..."  % self.config.outputpath
      shutil.rmtree( self.config.outputpath )

    print "@ Creating '%s' path ..." % self.config.outputpath
    os.mkdir( self.config.outputpath )

    for source, destination in self.config.copypaths.items():
      print "@ Importing '%s' to '%s' ..." % (source, destination)
      if os.path.isfile(source):
        shutil.copy( source, destination )
      elif os.path.isdir(source):
        shutil.copytree( source, destination )
      else:
        raise Exception("Unexpected type of '%s' ." % source )

    if os.path.exists( os.path.join( self.config.tplpath, 'index.tpl' ) ):
      print "@ Creating index file ..."
      index = Page( 'index', 'index.tpl' ).setCustom( 'pages', pages )
      index.create()
    else:
      raise Exception( "No index template found." )

    if os.path.exists( os.path.join( self.config.tplpath, '404.tpl' ) ):
      print "@ Creating 404 file ..."
      Page( '404', '404.tpl' ).setCustom( 'pages', pages ).create()

    if os.path.exists( os.path.join( self.config.tplpath, 'feed.tpl' ) ):
      print "@ Creating feed.xml file ..."
      feed = Page( 'feed', 'feed.tpl' )
      feed.setCustom( 'pages', pages )
      feed.extension = 'xml'
      feed.create()

    print "@ Rendering %d pages ..." % len(pages)
    for page in pages:
      page.setCustom( 'pages', pages ).create()

    if os.path.exists( os.path.join( self.config.tplpath, 'sitemap.tpl' ) ):
      print "@ Creating sitemap.xml file ..."
      sitemap = Page( 'sitemap', 'sitemap.tpl' )
      sitemap.setCustom( 'index', index )
      sitemap.setCustom( 'pages', pages )
      sitemap.extension = 'xml'
      sitemap.create()

    if self.config.gzip is True:
      htaccess = os.path.join( self.config.outputpath, '.htaccess' ) 
      if os.path.exists( htaccess ):
        fd = open( htaccess, "a+t" )
        fd.write( """
  # SWG Generated Code
  AddEncoding gzip .gz
  DirectoryIndex index.html index.htm index.shtml index.php index.php4 index.php3 index.phtml index.cgi index.html.gz

  <Files *.""" + self.config.page_ext + """.gz>
    ForceType text/html
  </Files>

  <FilesMatch .*\.(""" + self.config.page_ext + """)>
    RewriteEngine on
    RewriteCond %{REQUEST_FILENAME}.gz -f
    RewriteRule ^(.*)$ $1.gz [L]
  </FilesMatch>""" )
        fd.close()
      else:
        fd = open( htaccess, "w+t" )
        fd.write( """
  # SWG Generated Code
  Options +FollowSymlinks
  RewriteEngine on

  AddEncoding gzip .gz
  DirectoryIndex index.html index.htm index.shtml index.php index.php4 index.php3 index.phtml index.cgi index.html.gz

  <Files *.""" + self.config.page_ext + """.gz>
    ForceType text/html
  </Files>

  <FilesMatch .*\.(""" + self.config.page_ext + """)>
    RewriteEngine on
    RewriteCond %{REQUEST_FILENAME}.gz -f
    RewriteRule ^(.*)$ $1.gz [L]
  </FilesMatch>""" )
        fd.close()

    print "@ DONE\n"

    if self.config.transfer is not None:
      os.system( self.config.transfer.encode( "UTF-8" ) )
    else:
      for filename, info in DiffManager.getInstance().changes.items():
        ( digest, status ) = info
        print "@ %-8s : '%s'" % ( status, filename.encode( "UTF-8" ) )

