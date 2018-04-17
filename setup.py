from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fmDataAPI',
    version='1.0.2',
    description='a Python library for interacting with the FileMaker Data API',
    long_description=long_description,
    url='https://github.com/peterldowns/mypackage',
    author='Eric Luce',
    author_email='eluce@huntington.edu',
    install_requires=['json', 'requests'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    keywords='filemaker helper',
    packages=find_packages()
)

