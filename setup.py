#!/usr/bin/env python
install_requires = ['numpy', 'scipy']
tests_require=['nose','coveralls']
# %%
from setuptools import setup, find_packages

setup(name='radioutils',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      description=('Low-level radio communications modeling utilities'
                   'including AM, FM, SSB/DSB demodulation of GNU Radio data'),
      url='https://github.com/scivision/radioutils',
      classifiers=[
          'Intended Audience :: Science/Research',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Programming Language :: Python :: 3',
      ],
      install_requires=install_requires,
      tests_require=tests_require,
      version='1.5.0',
      extras_require={'plot':['matplotlib','seaborn'],
                      'io':['pygame'],
                      'tests':tests_require},
      python_requires='>=3.6',
      )
