import multiprocessing
from setuptools import setup, find_packages
import os
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "GoogleTrends",
    version = "0.1",
    packages = find_packages(),

    # Dependencies on other packages:
    # Couldn't get numpy install to work without
    # an out-of-band: sudo apt-get install python-dev
    setup_requires   = ['pytest-runner'],
    install_requires = ['pytrends>=4.7.3',
                        'pandas>=1.1.1',
                        'matplotlib>=3.3.1',
                        ],

    #dependency_links = ['https://github.com/DmitryUlyanov/Multicore-TSNE/tarball/master#egg=package-1.0']
    # Unit tests; they are initiated via 'python setup.py test'
    #test_suite       = 'nose.collector',
    #test_suite       = 'tests',
    #test_suite        = 'unittest2.collector',
    tests_require    =['pytest',
                       'testfixtures>=6.14.1',
                       ],

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "Accessing Google Trends using pytrends package",
    long_description_content_type = "text/markdown",
    long_description = long_description,
    license = "BSD",
    keywords = "trends",
    url = "https://github.com/paepcke/google_trends_access.git",   # project home page, if any
)
