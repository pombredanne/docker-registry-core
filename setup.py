#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import setuptools
except ImportError:
    import distutils.core as setuptools

import sys

from lib.core import __author__
from lib.core import __email__
from lib.core import __maintainer__
from lib.core import __title__
from lib.core import __version__

if sys.version_info < (2, 6):
    raise Exception("Docker registry requires Python 2.6 or higher.")

requirements_txt = open('./requirements.txt')
requirements = [line for line in requirements_txt]

ver = sys.version_info

# 2.6 native json raw_decode doesn't fit the bill, so add simple to our req
if ver[0] == 2 and ver[1] <= 6:
    requirements.insert(0, 'simplejson')

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    url='https://github.com/dmp42/droid-core',
    description="Backend drivers for the docker registry",
    long_description=open('./README.md').read(),
    download_url='https://github.com/dmp42/droid-core/archive/master.zip',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Operating System :: OS Independent',
                 'Topic :: Utilities',
                 'License :: OSI Approved :: Apache Software License'],
    # platforms=['Independent'],
    license=open('./LICENSE').read(),
    namespace_packages=['droid', 'droid.drivers'],
    package_dir={'droid': 'lib'},
    packages=['droid', 'droid.core', 'droid.drivers', 'droid.tests'],
    install_requires=requirements,
    zip_safe=True,
    setup_requires=['nose', 'flake8'],
    test_suite='nose.collector'
)
