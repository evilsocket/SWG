from swg.core.config import Config
from setuptools import setup, find_packages
from distutils.util import convert_path
from fnmatch import fnmatchcase

import shutil
import os
import sys

def get_data_files():
    data = []
    for folder, subdirs, files in os.walk( 'swg/basic/db/' ):
        for fname in files:
            if fname[0] != '.' and fname.endswith('.swp') == False:
                data.append( os.path.join( folder, fname ) )
    
    return data

try:
  long_description = open( 'README.md', 'rt' ).read()
except:
  long_description = 'SWG - A static website generator'

setup( name                 = 'swg',
       version              = Config.version,
       description          = 'SWG - A static website generator',
       long_description     = long_description,
       author               = 'Simone Margaritelli',
       author_email         = 'evilsocket@gmail.com',
       url                  = 'http://www.github.com/evilsocket/swg',
       packages             = find_packages(),
       include_package_data = True,
       package_data         = { 'swg': get_data_files() },
       install_requires     = ( 'mako >= 0.4.1', 'markdown' ),
       dependency_links     = [ 'http://cctools.svn.sourceforge.net/svnroot/cctools/vendorlibs/utidylib/#egg=utidylib-0.2-cvs' ],
       scripts              = [ 'swg/swg', 'swg/swg-wordpress' ],
       license              = 'GPL',
       zip_safe             = False,
       classifiers          = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Unix',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Code Generators',
            'Topic :: Internet',
            'Topic :: Internet :: WWW/HTTP :: Site Management',
            'Natural Language :: English'
      ]
)

