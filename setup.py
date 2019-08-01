# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""ORCID integration for Invenio."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.4.2',
    ],
    # Elasticsearch version
    'elasticsearch2': [
        'elasticsearch>=2.0.0,<3.0.0',
        'elasticsearch-dsl>=2.0.0,<3.0.0',
    ],
    'elasticsearch5': [
        'elasticsearch>=5.0.0,<6.0.0',
        'elasticsearch-dsl>=5.1.0,<6.0.0',
    ],
    'elasticsearch6': [
        'elasticsearch>=6.0.0,<7.0.0',
        'elasticsearch-dsl>=6.0.0,<6.2.0',
    ],
    'elasticsearch7': [
        'elasticsearch>=7.0.0,<8.0.0',
        'elasticsearch-dsl>=7.0.0,<8.0.0',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name in ('elasticsearch2', 'elasticsearch5',
                'elasticsearch6', 'elasticsearch7'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask>=0.11.1',
    'Flask-BabelEx>=0.9.2',
    'invenio-db>=1.0.0a9',
    'invenio-oauthclient>=1.0.0a4',
    'orcid>=0.7.0',
    'invenio-records-rest>=1.0.0',
    'invenio-search>=1.0.0'
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_orcid', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-orcid',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio ORCID',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-orcid',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_orcid = invenio_orcid:InvenioORCID',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_orcid',
        ],
        # TODO: Edit these entry points to fit your needs.
        # 'invenio_access.actions': [],
        # 'invenio_admin.actions': [],
        # 'invenio_assets.bundles': [],
        # 'invenio_base.api_apps': [],
        # 'invenio_base.api_blueprints': [],
        'invenio_base.blueprints': [
            'invenio_orcid = invenio_orcid.views:blueprint',
        ],
        # 'invenio_celery.tasks': [],
        # 'invenio_db.models': [],
        # 'invenio_pidstore.minters': [],
        # 'invenio_records.jsonresolver': [],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 1 - Planning',
    ],
)
