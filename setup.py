from swg.core.config import Config
from setuptools import setup, find_packages
from distutils.util import convert_path
from fnmatch import fnmatchcase

import shutil
import os
import sys

def find_package_data( where               = '.', 
                       package             = '',
                       exclude             = ( '*.pyc', '*~', '*.bak', '*.swp*', '.*'),
                       exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info'),
                       only_in_packages    = True,
                       show_ignored        = False):

  out = {}
  stack = [(convert_path(where), '', package, only_in_packages)]
  while stack:
    where, prefix, package, only_in_packages = stack.pop(0)
    for name in os.listdir(where):
      fn = os.path.join(where, name)
      if os.path.isdir(fn):
        bad_name = False
        for pattern in exclude_directories:
          if (fnmatchcase(name, pattern) or fn.lower() == pattern.lower()):
            bad_name = True
            if show_ignored:
                print >> sys.stderr, ("Directory %s ignored by pattern %s" % (fn, pattern))
            break
            if bad_name:
              continue
            if os.path.isfile(os.path.join(fn, '__init__.py')):
              if not package:
                  new_package = name
              else:
                  new_package = package + '.' + name
              stack.append((fn, '', new_package, False))
            else:
              stack.append((fn, prefix + name + '/', package, only_in_packages))
          elif package or not only_in_packages:
            # is a file
            bad_name = False
            for pattern in exclude:
              if (fnmatchcase(name, pattern) or fn.lower() == pattern.lower()):
                bad_name = True
                if show_ignored:
                  print >> sys.stderr, ( "File %s ignored by pattern %s" % (fn, pattern))
                break
            if bad_name:
              continue
            out.setdefault(package, []).append(prefix+name)

      return out

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
       package_data         = find_package_data( package = 'swg', only_in_packages = False ),
       install_requires     = ( 'mako >= 0.4.1', 'dateutils >= 0.5.0', 'pytidylib >= 0.2.1' ),
       scripts              = [ 'swg/swg' ],
       license              = 'GPL',
       zip_safe             = False,
       classifiers          = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
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
      ]
)

