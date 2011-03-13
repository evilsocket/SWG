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
#!/usr/bin/python

import os
import re
import shutil

from optparse import OptionParser
from core.config     import Config
from core.pageparser import PageParser
from entities.page   import Page

oparser = OptionParser( usage = "usage: %prog <configuration file>\n" )

(options, args) = oparser.parse_args()

print "- SWG 1.0.0 by Simone 'evilsocket' Margaritelli <evilsocket@gmail.com> -\n"

try:

  if len(args) < 1:
    oparser.error( "No configuration file specified!" )
  else:
    configfile = args[0].strip()

  Config.getInstance().load(configfile)

  parser = PageParser( )
  files  = os.listdir( Config.getInstance().dbpath + "/pages/" )
  pages  = []

  print "@ Parsing pages ..."
  for file in files:
    if re.match( '^.+\.' + Config.getInstance().dbitem_ext + '$', file ):
      page = parser.parse( Config.getInstance().dbpath + "/pages/" + file )
      pages.append(page)

  print "@ Sorting pages by date ..."
  pages.sort( reverse=True, key=lambda p: p.datetime )

  # delete output directory and recreate it
  if os.path.exists( Config.getInstance().outputpath ):
    print "@ Removing old '%s' path ..." % Config.getInstance().outputpath
    shutil.rmtree( Config.getInstance().outputpath )

  print "@ Creating '%s' path ..." % Config.getInstance().outputpath
  os.mkdir( Config.getInstance().outputpath )

  for source, destination in Config.getInstance().copypaths.items():
    print "@ Importing '%s' to '%s' ..." % (source, destination)
    if os.path.isfile(source):
      shutil.copy( source, destination )
    elif os.path.isdir(source):
      shutil.copytree( source, destination )
    else:
      raise Exception("Unexpected type of '%s' ." % source )

  if os.path.exists( Config.getInstance().tplpath + '/index.tpl' ):
    print "@ Creating index file ..."
    Page( 'index', 'index.tpl' ).setCustom( 'pages', pages ).create()
  else:
    raise Exception( "No index template found." )

  if os.path.exists( Config.getInstance().tplpath + '/404.tpl' ):
    print "@ Creating 404 file ..."
    Page( '404', '404.tpl' ).setCustom( 'pages', pages ).create()

  if os.path.exists( Config.getInstance().tplpath + '/sitemap.tpl' ):
    print "@ Creating sitemap.xml file ..."
    sitemap = Page( 'sitemap', 'sitemap.tpl' )
    sitemap.setCustom( 'pages', pages )
    sitemap.extension = 'xml'
    sitemap.create()

  if os.path.exists( Config.getInstance().tplpath + '/feed.tpl' ):
    print "@ Creating feed.xml file ..."
    feed = Page( 'feed', 'feed.tpl' )
    feed.setCustom( 'pages', pages )
    feed.extension = 'xml'
    feed.create()

  print "@ Rendering %d pages ..." % len(pages)
  for page in pages:
    page.setCustom( 'pages', pages ).create()

  print "@ DONE"
  
except Exception as e:
	print "! %s" % e