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
import math

from swg.core.config import Config

class Pager:
  def __init__( self, firstpage, format ):
    self.current   = 0
    self.pagen     = 0
    self.firstpage = firstpage
    self.format    = format
    self.pages     = []
    self.max       = 0
    self.left      = 0
    self.total     = 0
    self.config    = Config.getInstance()

  def setPages( self, pages ):
    self.pages = pages
    self.max   = len(pages)
    self.left  = self.max
    self.total = math.ceil( self.max / self.config.items_per_page )
    self.total += 1 if self.max % self.config.items_per_page != 0 else 0
    self.total = int(self.total)
    
  def getCurrentPageFilename(self):
    return self.format % self.pagen if self.pagen != 1 else self.firstpage

  def getCurrentPageNumber(self):
    return self.pagen

  def getTotalPages(self):
    return self.total

  def getCurrentPages(self):
    begin = (self.pagen - 1) * self.config.items_per_page
    end   = (begin + self.config.items_per_page) if self.left > self.config.items_per_page else (begin + self.left)
    return self.pages[begin:end]

  def goToNext(self):
    self.left = self.max - self.current
    if self.left <= 0:
      return False
    else:
      self.current += self.config.items_per_page if self.left > self.config.items_per_page else self.left
      return True

  def __iter__(self):
    return self

  def next(self):
    if self.goToNext() == False:
      raise StopIteration
    else:
      self.pagen += 1
      return self.getCurrentPageFilename()
