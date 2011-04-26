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
import os
import re
import sys
import urllib
import codecs
from xml.dom  import minidom
from datetime import datetime
from optparse import OptionParser

def slugify_name( name ):
  result = []
  for word in slugify.split( name.lower() ):
    result.extend( word.split() )

  return '-'.join(result)

print "- SWG Wordpress Backup Importer -\n"

parser = OptionParser( usage = "usage: %prog -i wordpress-backup.xml -u 'http://www.your-site-url.com' <options>\n" )

parser.add_option( "-i", "--input",	action="store", dest="wpbackup", default=None,  help="The Wordpress XML backup file." )
parser.add_option( "-u", "--url", 	action="store", dest="siteurl",  default=None,  help="URL of the destination website." )
parser.add_option( "-o", "--output",	action="store", dest="outdir",   default=".",   help="Output directory, default is the current working directory." )
parser.add_option( "-e", "--extension", action="store", dest="fileext",  default="txt", help="Output file extension, default is txt." )
parser.add_option( "-I", "--images",    action="store", dest="imgdir",   default=None,  help="If specified, it's the path where the importer will try to download images referenced by articles." )

(o,args) = parser.parse_args()

if o.wpbackup is None:
  parser.error( "Wordpress XML backup file not specified !")
elif o.siteurl is None:
  parser.error( "URL of the destination website not specified !" )

wpbackup    = o.wpbackup 
siteurl     = o.siteurl
fileext     = o.fileext
outdir      = o.outdir
imgdir      = o.imgdir
imgdownload = True if imgdir is not None else False

print "@ Loading %s ..." % wpbackup

doc     = minidom.parse(wpbackup)
items   = doc.getElementsByTagName('item')
domain  = re.sub( '^(https?\://)?(www\.)?', '', siteurl )
imgtag  = re.compile( '<\s*img[^/>]+src\s*=\s*[\'"]([^\'"]+' + re.escape(domain) + '[^\'"]+)[\'"]',re.IGNORECASE )
slugify = re.compile( r'[^\w]+' )

post_id         = 0
site_authors    = []
site_categories = []

# create needed directories
if not os.path.exists(outdir):
  os.mkdir( outdir )       

try:
  os.makedirs( outdir + os.sep + 'db' + os.sep + 'pages' )
except:
  pass

if imgdownload is True and not os.path.exists(imgdir):
  os.mkdir( imgdir )

for item in items:
  status = item.getElementsByTagName('wp:status')[0].firstChild.nodeValue
  type   = item.getElementsByTagName('wp:post_type')[0].firstChild.nodeValue
  # import only published posts
  if status == 'publish' and type == 'post':
    title      = item.getElementsByTagName('title')[0].firstChild.nodeValue
    date       = item.getElementsByTagName('wp:post_date')[0].firstChild.nodeValue
    author     = item.getElementsByTagName('dc:creator')[0].firstChild.nodeValue
    content    = item.getElementsByTagName('content:encoded')[0].firstChild.nodeValue
    categories = []
    tags       = []

    print "@ Processing '%s' ..." % title

    # get item categories and tags
    metas = item.getElementsByTagName('category')
    for meta in metas:
      domain = meta.attributes['domain'].value if meta.attributes.has_key('domain') else 'category'
      value  = meta.firstChild.nodeValue.strip()
      
      if domain == 'category' and value not in categories:
        categories.append(value)
      elif domain == 'tag' and value not in tags:
        tags.append(value)
        
    # replace the 'more' pseudo tag in the content with swg <break> 
    content = content.replace( '<!--more-->', '<break>' )
    # make sure date is correct attempting to parse it
    date    = datetime.strptime( date, '%Y-%m-%d %H:%M:%S' )
    # search for images to download
    if imgdownload is True:
      images = imgtag.findall(content)
      for image in images:
        # update the html with the new image url and download it to the specified directory
        imgname = os.path.basename(image)
        content = content.replace( image, siteurl + '/' + os.path.basename(imgdir) + '/' + imgname )
        imgfile = imgdir + os.sep + imgname 
        if not os.path.exists(imgfile):
          print "\t- downloading '%s' to %s ..." % ( image, imgfile )
          urllib.urlretrieve( image, imgfile )

    data = """\
Date: %s
Author: %s
Categories: %s
Tags: %s
Title: %s\n\n""" % ( date.strftime('%Y-%m-%d %H:%M:%S'), author, ', '.join(categories), ', '.join(tags), title ) + content
  
    filename = outdir + os.sep + 'db' + os.sep + 'pages' + os.sep + "%d.%s" % ( post_id, fileext )
    file     = codecs.open( filename, "w+", "utf-8")
    file.write(data)
    file.close()

    print "@ Saved to %s ." % filename

    # save author if not already present in the list
    if author not in site_authors:
      site_authors.append(author)
    # same for the categories
    for category in categories:
      if category not in site_categories:
        site_categories.append(category)

    post_id += 1
   
print
# create files for categories and authors
for author in site_authors:
  filename = outdir + os.sep + 'db' + os.sep + "%s.%s" % ( slugify_name(author), fileext )
  
  print "@ Creating author file %s ..." % filename
  
  file = codecs.open( filename, "w+", "utf-8")
  file.write( """\
username: %s
avatar: put your avatar url here
email: put your email here
website: %s

put a description of yourself here""" % ( author, siteurl ) )
  file.close()

filename = outdir + os.sep + 'db' + os.sep + "categories.%s" % fileext
file     = codecs.open( filename, "w+", "utf-8")
print "@ Creating categories file %s ..." % filename
for category in site_categories:
  file.write( category + "\n" )
file.close()

print "\n@ Done :)"
