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

from swg.core.config import Config
from swg.core.pager  import Pager

class Item:
    SLUGIFY_SPLIT_REGEXP  = re.compile( r'[^\w]+' )
    PAGER_ENABLED_CLASSES = (
        'swg.entities.category.Category',
        'swg.entities.tag.Tag',
        'swg.entities.author.Author'
    )

    def __init__( self, path, title, extension ):
        self.path        = path.replace( '//', '/' ) 
        self.title       = title.strip()
        self.extension   = extension.strip()
        self.name        = self.__generate_name()
        self.url         = ("%s/%s.%s" % (self.path,self.name,self.extension)).replace( '//', '/' )
        self.objects     = {}
        self.npages      = 1

    def __generate_name( self ):
        result = []
        for word in Item.SLUGIFY_SPLIT_REGEXP.split( self.title.lower() ):
            result.extend( word.split() )

        return '-'.join(result)

    def __save_contents( self, filename, contents ):
        fd = open( filename.encode('UTF-8'), "w+b" )
        fd.write( contents )
        fd.close()
    
    def addObject( self, name, value ):
        self.objects[name] = value
        
        if hasattr( self, 'author') and self.author is not None:
            self.author.addObject( name, value )
        
        if hasattr( self, 'categories' ):
            for category in self.categories:
                category.addObject( name, value )
        
        if hasattr( self, 'tags' ):
            for tag in self.tags:
                tag.addObject( name, value )

        return self

    def addObjects( self, dictionary ):
        for name, value in dictionary.items():
            self.addObject( name, value )
    
        return self

    def create(self):  
        config = Config.getInstance()
        path   = "%s%s%s" % ( config.outputpath, os.sep, self.path )

        if not os.path.exists( path ):
            os.mkdir(path)

        if config.pager == True and (self.title == 'index' or str(self.__class__) in Item.PAGER_ENABLED_CLASSES):     
            pager = Pager( '%s.%s'     % ( self.name, self.extension ),
                                          '%s-%%d.%s' % ( self.name, self.extension ) )
            
            if hasattr( self, 'items' ):
                pager.setPages( self.items )
            else:
                pager.setPages( self.objects['pages'] )

            self.npages = pager.getTotalPages()

            self.addObject( 'pager', pager )

            for filename in pager:
                filename = os.path.join( path, filename )
                content  = self.render()
                
                self.__save_contents( filename, content )
        else:
            filename = os.path.join( path, "%s.%s" % (self.name, self.extension) )
            content  = self.render()

            self.__save_contents( filename, content )
