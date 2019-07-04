#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Setup Module for Identity Access Package"""

from __future__ import absolute_import, print_function

# Standard Library Imports
from glob import glob
from os.path import basename, splitext

# ThirdParty Library Imports
from setuptools import find_packages, setup


setup(
    name='protean-realworld',
    version='0.0.1',
    license='BSD 3-Clause License',
    description='Realworld Implementation in Protean',
    long_description='Realworld Implementation in Protean',
    author='Subhash Bhushan C',
    author_email='subhash@team8solutions.com',
    url='https://github.com/proteanhq/samples/tree/master/realworld',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
