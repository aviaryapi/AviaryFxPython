# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import re
from distutils.core import setup

version_re = re.compile(
    r'__version__ = (\(.*?\))')

cwd = os.path.dirname(os.path.abspath(__file__))
fp = open(os.path.join(cwd, 'aviaryfx', '__init__.py'))

version = None
for line in fp:
    match = version_re.search(line)
    if match:
        version = eval(match.group(1))
        break
else:
    raise Exception('Cannot find version in __init__.py')
fp.close()

setup(name = 'AviaryFX',
	  version = '.' . join(map(str, version)),
	  description = 'AviaryFX Python SDK',
	  author = 'Bruce Drummond',
	  author_email = 'bruce@aviary.com',
	  license = 'GPL',
	  url = 'http://www.aviary.com',
	  packages = ['AviaryFX'],
	  provides = ['AviaryFX'], 
	  
	  classifiers = [
		  'Development Status :: 1 - Beta',
		  'Environment :: Console',
		  'Intended Audience :: Developers',
		  'License :: OSI Approved :: GNU General Public License (GPL)',
		  'Operating System :: OS Independent',
		  'Programming Language :: Python',
		  'Topic :: Software Development :: Libraries :: Python Modules',
	],
)