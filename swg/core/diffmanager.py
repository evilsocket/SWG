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
import codecs

from swg.core.config import Config

class DiffManager:
  __instance = None

  def __init__(self):
    self.changes  = {}
    self.sitename = Config.getInstance().sitename
    self.home     = os.path.expanduser( "~/.swg/" )
    self.sitebase = self.home + self.sitename + os.sep

    if not os.path.exists(self.home):
      os.mkdir(self.home)

    if not os.path.exists(self.sitebase):
      os.mkdir(self.sitebase)


  def __save_digest( self, digest_path, digest ):
    fd = codecs.open( digest_path, "w+", "utf-8" )
    fd.write( digest.strip() )
    fd.close()

  def checkItem( self, filename, hash_id, digest ):
    # a new file
    if not os.path.exists( self.sitebase + hash_id ):
      self.changes[filename] = ( digest, 'NEW' )
      self.__save_digest( self.sitebase + hash_id, digest )
    # existing file, check digests
    else:
      fd = codecs.open( self.sitebase + hash_id, "r", "utf-8" )

      old_digest = fd.read().strip()
      # changes!
      if digest != old_digest:
        self.changes[filename] = ( digest, 'MODIFIED' )
        self.__save_digest( self.sitebase + hash_id, digest )
          
      fd.close()

  @classmethod
  def getInstance(cls):
    if cls.__instance is None:
      cls.__instance = DiffManager()
    return cls.__instance
