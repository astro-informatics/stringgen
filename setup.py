import os
import shutil
from setuptools import setup

import numpy

# clean previous build
for root, dirs, files in os.walk("./cosmic_string_emulator/", topdown=False):
    for name in dirs:
        if (name == "build"):
            shutil.rmtree(name)

from os import path
this_directory = path.abspath(path.dirname(__file__))

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()

long_description = read_file("README.md")
required = read_requirements("requirements.txt")


include_dirs = [numpy.get_include(),]

extra_link_args=[]

setup(
    classifiers=['Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research'
                 ],
    name = "cosmic_string_emulator",
    version = "0.0.1",
    prefix='.',
    url='https://github.com/astro-informatics/cosmic_string_emulator',
    author='Matthew Price, Matthijs Mars, Matthew Docherty, Alessio Spurio Mancini, Auggie Marignier, Jason McEwen',
    # author_email='',
    # license='GNU General Public License v3 (GPLv3)',
    install_requires=required,
    description='Cosmic String Emulator',
    long_description_content_type = "text/markdown",
    long_description=long_description,
    packages=['cosmic_string_emulator', 'cosmic_string_emulator.data'],
    package_data={
        "cosmic_string_emulator.data":[
            "features_Price_et_al_2022.pkl",
        ],
    }
)