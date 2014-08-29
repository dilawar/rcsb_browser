import os
import sys

from setuptools import setup

with open("README.md") as f:
    readme = f.read()
classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    ]

setup(
    name = "rcsb_browser",
    version = "0.0.1",
    description = "Command line browser for RCSB database",
    long_description = readme,
    packages = ["browser", "downloader" ],
    package_data = {},
    install_requires = [ ],
    author = "Dilawar Singh",
    author_email = "dilawars@ncbs.res.in",
    url = "http://github.com/dilawar/",
    license='GPL',
    classifiers=classifiers,
    entry_points = {
        'console_scripts': [
            'rcsb_browser = browser.main',
            ],
        },
)
