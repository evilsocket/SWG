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
from dateutil import parser as datetime_parser

from swg.core.config import Config

class ItemParser:
  PARSE_NONE_STATE = 0
  PARSE_INFO_STATE = 1
  PARSE_BODY_STATE = 2
  PARSE_DONE_STATE = 3

  BODY_ABSTRACT_BREAK = u'<break>'

  TIDY_OPTIONS = {  'alt-text'          : ' ',
                    'doctype'           : 'transitional',
                    'bare'              : 1,
                    'clean'             : 0,
                    'hide-comments'     : 1,
                    'join-classes'      : 1,
                    'join-styles'       : 1,
                    'output-xhtml'      : 1,
                    'quote-nbsp'        : 0,
                    'preserve-entities' : 1,
                    'show-errors'       : 0,
                    'show-warnings'     : 0,
                    'wrap'              : 0,
                    'sort-attributes'   : 'alpha',
                    'char-encoding'     : 'utf8',
                    'input-encoding'    : 'utf8',
                    'output-encoding'   : 'utf8',
                    'indent'            : 0,
                    'indent-spaces'     : 0,
                    'newline'           : 'LF',
                    'output-bom'        : 0,
                    'force-output'      : 1,
                    'quiet'             : 1,
                    'tidy-mark'         : 0,
                    'show-body-only'    : 1
                  }

  def __init__(self):
    self.info     = {}
    self.abstract = ""
    self.body     = ""
    self.state    = ItemParser.PARSE_NONE_STATE
    self.lineno   = 1

  def __parse_datetime( self, data ):
    return datetime_parser.parse(data)

  def __parse_string( self, data ):
    return data.strip()

  def __parse_array( self, data ):
    data  = data.strip()
    items = data.split(',')
    return map( lambda s: s.strip(), items )

  def parse( self, mandatory_fields_map, filename ):
    fd = codecs.open( filename, "r", "utf-8" )

    self.state = ItemParser.PARSE_INFO_STATE

    for line in iter(fd):
      if self.state == ItemParser.PARSE_INFO_STATE:
        line = line.strip()
        if line == '':
          self.state = ItemParser.PARSE_BODY_STATE
        else:
          ( info_id, info_data ) = line.split( ':', 1 )
          info_id   = info_id.strip().lower()
          info_data = info_data.strip()

          if mandatory_fields_map.has_key(info_id):
            type = mandatory_fields_map[info_id]
            if type == 'datetime':
              self.info[info_id] = self.__parse_datetime(info_data)
            elif type == 'string':
              self.info[info_id] = self.__parse_string(info_data)
            elif type == 'array':
              self.info[info_id] = self.__parse_array(info_data)

          else:
            raise Exception( "Unknown key %s on line %d." % ( info_id, self.lineno ) )

      elif self.state == ItemParser.PARSE_BODY_STATE:
        self.body += line
      else:
        raise Exception( "Unhandled parser state on line %d." % self.lineno )

      self.lineno += 1

    missing = filter( lambda x:x not in self.info.keys(), mandatory_fields_map.keys() )
    if missing != []:
      raise Exception( "Missing mandatory fields : %s" % ', '.join(missing) )

    if ItemParser.BODY_ABSTRACT_BREAK in self.body:
      ( self.abstract, therest ) = self.body.split( ItemParser.BODY_ABSTRACT_BREAK, 1 )
      self.body = self.abstract.strip() + '<br/><br/>' + therest.strip()
    else:
      self.abstract = self.body

    # Fix <break> pseudo attribute newlines
    self.body     = self.body.replace( "\n\n", "<br/><br/>" )
    self.abstract = self.abstract.replace( "\n\n", "<br/><br/>" )

    # Tidyfy abstract and body html and fix encoding errors
    if Config.getInstance().tidyfy is True:
      import tidy

      self.body     = tidy.parseString( self.body.encode( 'UTF-8',     'replace' ),     **ItemParser.TIDY_OPTIONS )
      self.abstract = tidy.parseString( self.abstract.encode( 'UTF-8', 'replace' ), **ItemParser.TIDY_OPTIONS )
      self.body     = str(self.body).decode('UTF-8')
      self.abstract = str(self.abstract).decode('UTF-8')

    fd.close()
