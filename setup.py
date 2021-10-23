from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'A simple Python wrapper for the Minecraft Server Status API.'

# Setting up
setup(
    name="api.mcsrvstat.py",
    version=VERSION,
    author="HitBlast",
    author_email="<hitblastlive@gmail.com>",
    url='https://github.com/hitblast/api.mcsrvstat.py',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'minecraft', 'mcsrvstat'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)