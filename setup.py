#!/usr/bin/env python
from distutils.core import setup
import pkg_resources
import geojoin

version = geojoin.VERSION

setup(name='geojoin',
      version=version,
      description='Merge CSV data into GeoJSON features, and more',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Text Processing :: Filters',
          'Topic :: Utilities'
      ],
      author='Shawn Allen',
      author_email='shawn@stamen.com',
      url='http://github.com/shawnbot/py-geojoin',
      packages=['geojoin'],
      requires=[
          'csv',
          'json'
      ],
      scripts=[
          'bin/geojoin'
      ],
      download_url='https://github.com/shawnbot/py-geojoin/archive/v%s.tar.gz' % version,
      license='BSD')
