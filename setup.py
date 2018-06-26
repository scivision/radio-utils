#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = ['numpy', 'scipy']
tests_require = ['pytest', 'coveralls', 'flake8', 'mypy']


setup(name='radioutils',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      description=('Low-level radio communications modeling utilities'
                   'including AM, FM, SSB/DSB demodulation of GNU Radio data'),
      long_description=open('README.rst').read(),
      url='https://github.com/scivision/radioutils',
      classifiers=[
          'Intended Audience :: Science/Research',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      install_requires=install_requires,
      tests_require=tests_require,
      version='1.5.2',
      extras_require={'plot': ['matplotlib', 'seaborn'],
                      'io': ['pygame'],
                      'tests': tests_require},
      python_requires='>=3.6',
      )
