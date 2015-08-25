#!/usr/bin/env python
import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "pyzbx"

PACKAGES = ["pyzbx",]

DESCRIPTION = "python get zabbix data api interface."

LONG_DESCRIPTION = read("README.md")

KEYWORDS = "get zabbix data api."

AUTHOR = "shaozhi.zhang"

AUTHOR_EMAIL = "davidbjhd@gmail.com"

URL = "https://github.com/davidbj/pyzbx"

VERSION = "0.0.1"

LICENSE = "MIT"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data = True,
    zip_safe = True,
)
