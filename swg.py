#!/usr/bin/python
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

oparser = OptionParser( usage = "usage: %prog <configuration file> (new)\n" )

(options, args) = oparser.parse_args()

print "- SWG 1.2.3 by Simone 'evilsocket' Margaritelli <evilsocket@gmail.com> -\n"

try:

  if len(args) < 1:
    oparser.error( "No configuration file specified!" )
  else:
    configfile = args[0].strip()

  Config.getInstance().load(configfile)

  config = Config.getInstance()  
  files  = os.listdir( config.dbpath + "/pages/" )
  
  if len(args) > 1 and args[1].lower() == 'new':
    maxid = 0;
    for file in files:
      ( id, ext ) = file.split('.')
      if int(id) > maxid:
        maxid = int(id);

    newitem = "%s/%d.%s" % ( config.dbpath + "/pages", maxid + 1, config.dbitem_ext )

    fd = open( newitem, 'w+t' )

    fd.write(
"""Date: %s
Author:
Categories:
Tags:
Title:

""" % config.now.strftime("%Y-%m-%d %H:%M:%S") )
    fd.close()
    
    os.system( "%s %s" % ( config.editor, newitem ) )

    if os.path.exists( newitem ):
      print "@ Item '%s' created, you can now regenerate the website ." % newitem
    else:
      print "@ Item was not saved, quitting ."
  else:
    parser = PageParser( )
    pages  = []

    print "@ Parsing pages ..."
    for file in files:
      if re.match( '^.+\.' + config.dbitem_ext + '$', file ):
        page = parser.parse( config.dbpath + "/pages/" + file )
        pages.append(page)

    print "@ Sorting pages by date ..."
    pages.sort( reverse=True, key=lambda p: p.datetime )

    # delete output directory and recreate it
    if os.path.exists( config.outputpath ):
      print "@ Removing old '%s' path ..." % config.outputpath
      shutil.rmtree( config.outputpath )

    print "@ Creating '%s' path ..." % config.outputpath
    os.mkdir( config.outputpath )

    for source, destination in config.copypaths.items():
      print "@ Importing '%s' to '%s' ..." % (source, destination)
      if os.path.isfile(source):
        shutil.copy( source, destination )
      elif os.path.isdir(source):
        shutil.copytree( source, destination )
      else:
        raise Exception("Unexpected type of '%s' ." % source )

    if os.path.exists( config.tplpath + '/index.tpl' ):
      print "@ Creating index file ..."
      index = Page( 'index', 'index.tpl' ).setCustom( 'pages', pages )
      index.create()
    else:
      raise Exception( "No index template found." )

    if os.path.exists( config.tplpath + '/404.tpl' ):
      print "@ Creating 404 file ..."
      Page( '404', '404.tpl' ).setCustom( 'pages', pages ).create()

    if os.path.exists( config.tplpath + '/feed.tpl' ):
      print "@ Creating feed.xml file ..."
      feed = Page( 'feed', 'feed.tpl' )
      feed.setCustom( 'pages', pages )
      feed.extension = 'xml'
      feed.create()

    print "@ Rendering %d pages ..." % len(pages)
    for page in pages:
      page.setCustom( 'pages', pages ).create()

    if os.path.exists( config.tplpath + '/sitemap.tpl' ):
      print "@ Creating sitemap.xml file ..."
      sitemap = Page( 'sitemap', 'sitemap.tpl' )
      sitemap.setCustom( 'index', index )
      sitemap.setCustom( 'pages', pages )
      sitemap.extension = 'xml'
      sitemap.create()

    if config.gzip is True:
      htaccess = "%s/.htaccess" % config.outputpath
      if os.path.exists( htaccess ):
        fd = open( htaccess, "a+t" )
        fd.write( """
  # SWG Generated Code
  AddEncoding gzip .gz
  DirectoryIndex index.html index.htm index.shtml index.php index.php4 index.php3 index.phtml index.cgi index.html.gz

  <Files *.""" + config.page_ext + """.gz>
    ForceType text/html
  </Files>

  <FilesMatch .*\.(""" + config.page_ext + """)>
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

  <Files *.""" + config.page_ext + """.gz>
    ForceType text/html
  </Files>

  <FilesMatch .*\.(""" + config.page_ext + """)>
    RewriteEngine on
    RewriteCond %{REQUEST_FILENAME}.gz -f
    RewriteRule ^(.*)$ $1.gz [L]
  </FilesMatch>""" )
        fd.close()

    print "@ DONE\n"

    if config.transfer is not None:
      os.system( config.transfer.encode( "UTF-8" ) )
    else:
      for filename, info in DiffManager.getInstance().changes.items():
        ( digest, status ) = info
        print "@ %-8s : '%s'" % ( status, filename.encode( "UTF-8" ) )

except Exception as e:	
  raise
