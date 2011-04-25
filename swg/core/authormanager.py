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

from swg.core.authorparser import AuthorParser
from swg.core.config       import Config

class AuthorManager:
  __instance = None

  def __init__(self):
    self.authors = {}

  def get( self, username ):
    id = username.lower()
    if not self.authors.has_key(id):
      self.authors[id] = AuthorParser().parse( os.path.join( Config.getInstance().dbpath, ( "%s.%s" % (username,Config.getInstance().dbitem_ext) ) ) )

    return self.authors[id]

  @classmethod
  def getInstance(cls):
    if cls.__instance is None:
      cls.__instance = AuthorManager()
    return cls.__instance
