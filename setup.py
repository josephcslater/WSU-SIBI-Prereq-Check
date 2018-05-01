#!/usr/bin/env python

# from distutils.core import setup
import os
import sys
from setuptools import setup

if sys.version_info < (3, 5):
    sys.exit('Sorry, Python < 3.5 is not supported.')
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    """You want a docstring? Tell me why."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('prereqcheck/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break


setup(name='prereqcheck',
      version=version,
      description='Wright State prerequisite checking',
      author='Joseph C. Slater',
      author_email='joseph.c.slater@gmail.com',
      url='https://github.com/josephcslater/WSU-SIBI-Prereq-Check',
      download_url='https://github.com/josephcslater/WSU-SIBI-Prereq-Check',
      packages=['prereqcheck'],
      package_data={'prereqcheck': ['../README.rst'], '': ['README.rst']},
      long_description=read('README.rst'),
      keywords=[''],
      install_requires=['pandas'],
      setup_requires=['pytest-runner'],
      )

# https://docs.python.org/3/distutils/setupscript.html#additional-meta-data
