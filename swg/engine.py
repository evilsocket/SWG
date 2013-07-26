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
import time
import os.path
import re
import shutil
import SimpleHTTPServer
import SocketServer

from swg.core.config      import Config
from swg.core.pageparser  import PageParser
from swg.entities.page    import Page

class ProgressBar:
    def __init__( self, min_value = 0, max_value = 100, width = 77, char = '#' ):
        self.char   = char
        self.bar  = ''
        self.min  = min_value
        self.max  = max_value if max_value != None else 0
        self.span   = self.max - self.min
        self.width  = width
        self.amount = 0
        self.update_amount(0) 
  
    def increment_amount(self, add_amount = 1):
        new_amount = self.amount + add_amount
        if new_amount < self.min: new_amount = self.min
        if new_amount > self.max: new_amount = self.max
        self.amount = new_amount
        self.build_bar()
  
    def update_amount(self, new_amount = None):
        if not new_amount: new_amount = self.amount
        if new_amount < self.min: new_amount = self.min
        if new_amount > self.max: new_amount = self.max
        self.amount = new_amount
        self.build_bar()
  
    def build_bar(self):
        diff = float(self.amount - self.min)
        percent_done = int(round((diff / float(self.span)) * 100.0)) if self.max != 0 else 100
  
        # figure the proper number of 'character' make up the bar 
        all_full = self.width - 2
        num_hashes = int(round((percent_done * all_full) / 100))
  
        self.bar = self.char * num_hashes + ' ' * (all_full-num_hashes)
  
        percent_str = str(percent_done) + "%"
        self.bar = '[ ' + self.bar + ' ] ' + percent_str
  
    def __str__(self):
        return str(self.bar)
        
class Engine:
    __instance = None

    def __init__(self):
        self.config   = Config.getInstance()
        self.dbdir    = os.path.join( self.config.dbpath, 'pages' )
        self.files    = []
       
        if os.path.exists( self.dbdir ):
            for folder, subdirs, files in os.walk( self.dbdir ):
                for fname in files:
                    self.files.append( os.path.realpath( os.path.join( folder, fname ) ) ) 

        self.path     = os.path.dirname( os.path.realpath( __file__ ) )
        self.pages    = []
        self.progress = None
        self.statics  = None
        self.index    = None
        self.e404     = None
        self.sitemap  = None
        self.feed     = None

    def getPageByTitle( self, title, caseSensitive = True ):
        lwr_title = title.lower() if caseSensitive is False else None
        for page in self.pages:
            if page.title == title or (caseSensitive is False and page.title.lower() == lwr_title):
                return page

        return None

    def getStaticPages( self ):
        if self.statics is None:
            self.statics = filter( lambda page: page.static is True, self.pages )

        return self.statics

    def new( self ):
        newitem = os.path.join( self.dbdir, "%s.md" % self.config.now.strftime("%Y-%m-%d %H:%M:%S") )
        fd      = open( newitem, 'w+t' )

        fd.write( """\
Date: %s
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

    def create( self, destfolder ):
        if os.path.exists(destfolder):
            sys.exit( "@ The folder '%s' already exists, operation interrupted for security reasons." % destfolder )  
        else:
            print "@ Creating SWG basic website structure inside the '%s' folder ..." % destfolder

            shutil.copytree( os.path.join( self.path, 'basic' ), destfolder )

            print """\
@ Basic website initialized, now run:

    cd %s
    swg --generate

To generate the html contents or:

    cd %s
    swg --serve

To test the website locally.""" % (destfolder,destfolder)

    def serve( self ):

        class SWGServer(SocketServer.TCPServer):
            allow_reuse_address = True

        self.config.siteurl = 'http://localhost:8080'
        self.generate()

        os.chdir( self.config.outputpath )

        print "\n@ Serving the site on http://localhost:8080/ press ctrl+c to exit ..."
        
        try:
            SWGServer( ("",8080), SimpleHTTPServer.SimpleHTTPRequestHandler ).serve_forever()
        except KeyboardInterrupt:
            print "\n@ Bye :)"

    def generate( self ):
        start  = time.time( )
        parser = PageParser( )
        
        print "@ Parsing pages ..."
        for file in self.files:
            if re.match( '^.+\..+$', file ):
                filename = os.path.join( self.dbdir, file )
                page     = parser.parse( filename )
                self.pages.append(page)

        print "@ Sorting pages by date ..."
        self.pages.sort( reverse=True, key=lambda p: p.datetime )

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
            self.index = Page( 'index', 'index.tpl' )
            self.index.addObjects( { 'pages' : self.pages, 'swg' : self } )
            self.index.create()
        else:
            raise Exception( "No index template found." )

        if os.path.exists( os.path.join( self.config.tplpath, '404.tpl' ) ):
            print "@ Creating 404 file ..."
            self.e404 = Page( '404', '404.tpl' )
            self.e404.addObjects( { 'pages' : self.pages, 'swg' : self } )
            self.e404.create()

        if os.path.exists( os.path.join( self.config.tplpath, 'feed.tpl' ) ):
            print "@ Creating feed.xml file ..."
            self.feed = Page( 'feed', 'feed.tpl' )
            self.feed.addObjects( { 'pages' : self.pages, 'swg' : self } )
            self.feed.extension = 'xml'
            self.feed.create()
        
        self.progress = ProgressBar( 0, len(self.pages) )
        
        for page in self.pages:
            page.addObjects( { 'pages' : self.pages, 'swg' : self } ).create()
            self.progress.increment_amount()
            sys.stdout.write( "@ Rendering %d pages : %s\r" % ( len(self.pages), self.progress ) )
            sys.stdout.flush()
            
        self.progress.update_amount( len(self.pages) )
        sys.stdout.write( "@ Rendering %d pages : %s\r" % ( len(self.pages), self.progress ) )
        sys.stdout.flush()
        print "\n",

        if os.path.exists( os.path.join( self.config.tplpath, 'sitemap.tpl' ) ):
            print "@ Creating sitemap.xml file ..."
            self.sitemap = Page( 'sitemap', 'sitemap.tpl' )
            self.sitemap.addObjects( { 'index' : self.index, 'pages' : self.pages, 'swg' : self } )
            self.sitemap.extension = 'xml'
            self.sitemap.create()
    
        print "@ Website succesfully generated in %s .\n" % time.strftime('%H:%M:%S', time.gmtime( time.time() - start ) )

        if self.config.transfer is not None:
            os.system( self.config.transfer.encode( "UTF-8" ) )
        
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = Engine()
        return cls.__instance
