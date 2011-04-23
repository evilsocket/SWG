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
from engine import Engine

oparser = OptionParser( usage = "usage: %prog <configuration file> (new)\n" )

(options, args) = oparser.parse_args()

print "- SWG 1.2.3 by Simone 'evilsocket' Margaritelli <evilsocket@gmail.com> -\n"

try:

  if len(args) < 1:
    oparser.error( "No configuration file specified!" )
  else:
    configfile = args[0].strip()

  Config.getInstance().load(configfile)
  
  if len(args) > 1 and args[1].lower() == 'new':
    Engine().new()
  else:
    Engine().generate()  

except Exception as e:	
  raise
