# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 11:43:06 2014

@author: jmmauricio
"""

# tabulate, hickle, pyyaml, cython
import os
from setuptools import setup, find_packages
import pip
from pip.req import parse_requirements
from pip.download import PipSession
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = "0.2.0"

reqs = []

setup(
    name = "pypstools",
    packages = ['pypstools'], # this must be the same as the name above
    version = version,
    author = "Juan Manuel Mauricio",
    author_email = "jmmauricio6@gmail.com",
    description = ("Tools for power system studies tools"),
    long_description = """Tools for power system studies using DigSILENT or PSS/E""",
    license = "MIT",
    keywords = "dynamics model simulation pss/e digsilent",
    url = "https://github.com/jmmauricio/pypstools.git",
    download_url = 'https://github.com/jmmauricio/pypstools/tarball/{:s}'.format(version), # I'll explain this in a second
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires = reqs,
    
)