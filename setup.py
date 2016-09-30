# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'melomaniac/version.py')) as f:
        variables = {}
        exec(f.read(), variables)

        version = variables.get('VERSION')
        if version:
            return version

    raise RuntimeError('No version info found.')


__version__ = get_version()

setup(
    name='melomaniac',
    license='MIT',
    version=__version__,
    description='Listen to your Google Play Music/Soundcloud library from your terminal.',
    long_description=open('README.rst').read(),
    author='Sébastien Eustace',
    author_email='sebastien@eustace.io',
    url='https://github.com/sdispater/melomaniac',
    download_url='https://github.com/sdispater/melomaniac/archive/%s.tar.gz' % __version__,
    packages=['melomaniac'],
    install_requires=['cleo'],
    entry_points={
        'console_scripts': ['melomaniac=melomaniac.app:app.run'],
    },
    tests_require=['pytest'],
    test_suite='nose.collector',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
