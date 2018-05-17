from setuptools import setup, find_packages

setup(
    name='fmrest',
    version='1.0.6',
    description='a Python library for interacting with the FileMaker REST APIs',
    url='https://github.com/eluce2/fmrest',
    author='Eric Luce',
    author_email='eluce@huntington.edu',
    install_requires=['requests'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    keywords='filemaker helper rest api fmrest fmapi',
    packages=find_packages()
)
