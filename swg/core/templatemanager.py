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
from mako.lookup     import TemplateLookup
from swg.core.config import Config

import swg

class TemplateManager:
  __instance = None
    
  def __init__(self):
    config = Config.getInstance()

    self.lookup = TemplateLookup( directories     = [config.tplpath],
                                  output_encoding = 'utf-8',
                                  input_encoding  = 'utf-8',
                                  encoding_errors = 'replace',
                                  cache_enabled   = True,
                                  cache_type      = 'file',
                                  cache_dir       = config.tplcache,
                                  collection_size = 1024
                                )

  def get( self, name ):
    return self.lookup.get_template(name)

  @classmethod
  def render( cls, template, **kwargs ):
    return template.render( config     = Config.getInstance(),
                            categories = swg.core.categorymanager.CategoryManager.getInstance().get(),
                            tags       = swg.core.tagmanager.TagManager.getInstance().get(),
                            **kwargs )

      

  @classmethod
  def getInstance(cls):
    if cls.__instance is None:
      cls.__instance = TemplateManager()
    return cls.__instance
