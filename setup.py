# -*- coding:utf-8 -*-
#!/usr/bin/env Python

import os, datetime
from setuptools import find_packages
from assemtools.tool.setup import setup, on_version, on_description, on_requirement

setup(
    on_version('0.0.1', 'a'),
    on_description(),
    on_requirement(),

    name = "douya",
    author = 'xmyeen@163.com',
    author_email = "xmyeen@163.com",
    packages = find_packages(exclude = ["*.tests", "*.tests.*", "tests.*", "tests"]),
    platforms = ["all"],
    classifiers = [
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X"
    ],
    python_requires='>=3.8'
)