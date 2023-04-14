# -*- coding:utf-8 -*-
#!/usr/bin/env python

from assemtools import find_packages, setup, on_version, on_description, on_requirement

setup(
    on_version('0.0.2', dev_release='git'),
    on_description(),
    on_requirement(),

    name = "douya",
    author = 'xmyeen@163.com',
    author_email = "xmyeen@163.com",
    packages = find_packages(exclude = ["examples.*", "*.tests", "*.tests.*", "tests.*", "tests"]),
    platforms = ["all"],
    classifiers = [
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X"
    ],
    python_requires='>=3.11'
)