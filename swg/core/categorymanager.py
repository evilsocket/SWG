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
import codecs

from swg.entities.category import Category
from swg.core.config       import Config

class CategoryManager:
  __instance = None

  def __init__(self):
    self.categories = {}
    self.hierarchy  = []

  def get( self, title = None ):
    if title != None:
      id = title.lower()
      if not self.categories.has_key(id):
        self.categories[id] = Category(title)

      return self.categories[id]
    else:
      if self.hierarchy == []:
        self.__build_hierarchy()

      return self.hierarchy

  def __find_category( self, title ):
    for category in self.categories.values():
      if category.title == title:
        return category
    return None

  def __find_in_hyerarchy( self, title, node ):
    if node.title == title:
      return node
      
    for child in node.children:
      if child.title == title:
        return child
      else:
        found = self.__find_in_hyerarchy( title, child )
        if found != None:
          return found

    return None

  # only for debug purpose
  def __print_hierarchy(self,node,tabs = 0):
    print "%s%s :" % ( "\t" * tabs, node.title )
    for child in node.children:
      self.__print_hierarchy( child, tabs + 1 )

  def __build_hierarchy(self):
    fd = codecs.open( Config.getInstance().hierarchy, "r", "utf-8" )

    for line in iter(fd):
      line = line.strip()
      if line != '':
        if ':' in line:
          ( root, children ) = line.split( ':', 1 )
          root     = root.strip()
          children = [ s.strip() for s in children.strip().split(',') ]
        else:
          root     = line
          children = []

        h_root = None
        
        for category in self.hierarchy:
          h_root = self.__find_in_hyerarchy( root, category )
          if h_root != None:
            break

        if h_root == None:
          h_root = self.__find_category(root)
          if h_root != None:
            self.hierarchy.append(h_root)
       
        for child in children:
          h_child = self.__find_category(child)
          if h_root is not None and h_child is not None:
            h_root.children.append(h_child)

    fd.close()

  @classmethod
  def getInstance(cls):
    if cls.__instance is None:
      cls.__instance = CategoryManager()
    return cls.__instance
