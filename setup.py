# -*- coding: utf-8 -*-
# IDD3 - Propositional Idea Density from Dependency Trees
# Copyright (C) 2014  Andre Luiz Verucci da Cunha
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup, find_packages


def read(filename):
    """Read a file and return its contents.
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as infile:
        content = infile.read()

    return content


setup(
    name="IDD3",
    version="0.1.0",
    author="Andre Cunha",
    author_email="andre.lv.cunha@gmail.com",
    description=("IDD3 (Propositional Idea Density from Dependency Trees) is "
                 "a Python library that can extract propositions from a "
                 "sentence, given its dependency tree."),
    license="GPLv3",
    keywords="text analysis proposition",
    # url="http://packages.python.org/????",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ],
    install_requires = ['nltk >= 3.0.0',
                        ],
    extras_require = ['termcolor >= 1.1.0', ]
)
