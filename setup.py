"""
Setup for CRIkit2
"""

from setuptools import setup, find_packages
import crikit
# ! Need to change to rst in the future
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

# ! Set install_requires in check_requirements.py as well

print(crikit.__version__)

setup(name='CRIkit2',
      version = crikit.__version__,
      description = 'Hyperspectral imaging (HSI) processing and analysis platform (user interface, UI)',
      long_description = long_description,
      url = 'https://github.com/CCampJr/CRIkit2',
      author = 'Charles H. Camp Jr.',
      author_email = 'charles.camp@nist.gov',
      license = 'Public Domain',
      packages = find_packages(),
      entry_points={
          'gui_scripts': (
              'crikit2-start = crikit.__main__:main')},
      zip_safe = False,
      include_package_data = True,
      install_requires=['numpy','matplotlib','scipy','sciplot-pyqt>=0.2.2', 
                        'cvxopt','packaging'],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Environment :: X11 Applications :: Qt',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Scientific/Engineering :: Visualization'])
