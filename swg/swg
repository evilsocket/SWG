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
from swg.engine      import Engine
from swg.core.config import Config
from optparse        import OptionParser

print "- SWG %s by Simone 'evilsocket' Margaritelli <evilsocket@gmail.com> -\n" % Config.version

oparser = OptionParser( usage = "usage: %prog <action>\n" )

oparser.add_option( '-C', '--create',   action = 'store_const', const = 'create',   dest = 'action', help = 'Create a new website basic structure, require a folder name additional parameter.' )
oparser.add_option( '-N', '--new',      action = 'store_const', const = 'new',      dest = 'action', help = 'Create a new item and open an editor to edit it.' )
oparser.add_option( '-G', '--generate', action = 'store_const', const = 'generate', dest = 'action', help = 'Start website generation.' )
oparser.add_option( '-S', '--serve',    action = 'store_const', const = 'serve',    dest = 'action', help = 'Generate website and test it on http://localhost:8080/' )

(options, args) = oparser.parse_args()

try:
 
  if options.action is None:
    oparser.error( "No action specified, use --help to see a list of available actions." )
  elif options.action == 'create':
    if args == []:
      oparser.error( "No website folder specified, please use the syntax '--create website-folder-name'.")
    else:
      Engine().create( args[0].strip() )
  elif options.action == 'new':
    Config.getInstance().load('swg.cfg')
    Engine().new()
  elif options.action == 'serve':
    Config.getInstance().load('swg.cfg')
    Engine().serve()
  elif options.action == 'generate':
    Config.getInstance().load('swg.cfg')
    Engine().generate()  
  else:
    oparser.error( "%s invalid action!" % options.action )

except Exception as e:	
  raise
