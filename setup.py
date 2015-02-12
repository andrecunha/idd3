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
                        'prettytable >= 0.7.2'],
    extras_require = ['termcolor >= 1.1.0', ]
)
