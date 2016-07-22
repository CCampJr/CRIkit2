# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 01:11:04 2016

@author: chc
"""

from setuptools import setup, find_packages

setup(name='crikit2',
      version = '0.1',
      description = 'Hyperspectral imaging (HSI) processing and analysis \
      platform (user interface, UI)',
      url = 'https://github.com/CCampJr/crikit2',
      author = 'Charles H. Camp Jr.',
      author_email = 'charles.camp@nist.gov',
      license = 'NONLICENSE',
      packages = find_packages(),
      entry_points={
          'gui_scripts': (
              'crikit2-start = crikit.__main__:main')},
      zip_safe = False,
      include_package_data = True,
      install_requires=['numpy','matplotlib','yapsy','sciplot-pyqt>=0.1.2'],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Environment :: X11 Applications :: Qt',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Scientific/Engineering :: Visualization'])