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
from entities.item import Item
from core.config   import Config

import core.templatemanager

class Tag(Item):
  def __init__( self, title ):
    Item.__init__( self, Config.getInstance().basepath + "/tags", title, Config.getInstance().page_ext )
    self.title    = title
    self.items    = []
    self.template = core.templatemanager.TemplateManager.getInstance().get('tag.tpl')
    self.custom   = {}
    self.sorted   = False

  def setCustom( self, name, value ):
    self.custom[name] = value
    return self

  def render( self ):
    if not self.sorted:
      self.items.sort( reverse=True, key=lambda item: item.datetime )
      self.sorted = True

    return core.templatemanager.TemplateManager.render( template = self.template, tag = self, **self.custom )
