# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def get_version():
    with open(os.path.join(here, 'melomaniac/version.py')) as f:
        variables = {}
        exec(f.read(), variables)

        version = variables.get('VERSION')
        if version:
            return version

    raise RuntimeError('No version info found.')


__version__ = get_version()


with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.readlines()


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
    packages=find_packages(exclude=['tests']),
    install_requires=requirements,
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
