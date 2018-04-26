from setuptools import setup, find_packages

setup(
    name='dataAPI',
    version='1.0.3',
    description='a Python library for interacting with the FileMaker Data API',
    url='https://github.com/peterldowns/mypackage',
    author='Eric Luce',
    author_email='eluce@huntington.edu',
    install_requires=['requests'],
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

