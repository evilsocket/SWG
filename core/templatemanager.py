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
from core.config          import Config
from core.categorymanager import CategoryManager
from core.tagmanager      import TagManager
from mako.lookup          import TemplateLookup

class TemplateManager:
  __instance = None

  def __init__(self):
    self.lookup = TemplateLookup( directories     = [Config.getInstance().tplpath],
                                  output_encoding = 'utf-8',
                                  encoding_errors = 'replace' )

  def get( self, name ):
    return self.lookup.get_template(name)

  @classmethod
  def render( cls, template, **kwargs ):
    return template.render( config     = Config.getInstance(),
                            categories = CategoryManager.getInstance().get(),
                            tags       = TagManager.getInstance().get(),
                            **kwargs )

  @classmethod
  def getInstance(cls):
    if cls.__instance is None:
      cls.__instance = TemplateManager()
    return cls.__instance