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
import os, shutil, stat

if not os.geteuid() == 0:
  sys.exit( "Only root can run this script\n" )

srcpath = os.path.dirname( os.path.realpath( __file__ ) )
prefix  = '/usr'
dstpath = os.path.join( prefix, 'share', 'swg' )
dstbin  = os.path.join( prefix, 'bin',   'swg' )
items   = ( 'basic', 'importers', 'swg', 'LICENSE', 'README.md', 'swg.py' )

# Remove previous installations
if os.path.exists(dstpath):
  print "@ Removing old SWG installation ..."
  shutil.rmtree( dstpath )

# Install files
print "@ Creating directory %s ..." % dstpath
os.mkdir( dstpath )

for item in items:
  dest = os.path.join( dstpath, item )
  print "@ Installing %s to '%s' ..." % (item,dest)

  if os.path.isfile(item):
    shutil.copy( item, dstpath )
  else:
    shutil.copytree( item, dest ) 

# Set swg.py +x and create sysmlink 
print "@ Setting swg.py executable and creating symlink as %s ..." % dstbin

if os.path.exists(dstbin):
  os.unlink(dstbin)

script = os.path.join( dstpath, 'swg.py' )
mode   = os.stat(script)[stat.ST_MODE]
mode   = (mode | 0555) & 07777

os.chmod( script, mode )
os.symlink( script, dstbin )


