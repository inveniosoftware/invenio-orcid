# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Module tests."""

from __future__ import absolute_import, print_function

import json

from flask import Flask
from flask_babelex import Babel

from invenio_orcid import InvenioORCID
from invenio_orcid.views import blueprint


def test_version():
    """Test version import."""
    from invenio_orcid import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioORCID(app)
    assert 'invenio-orcid' in app.extensions

    app = Flask('testapp')
    ext = InvenioORCID()
    assert 'invenio-orcid' not in app.extensions
    ext.init_app(app)
    assert 'invenio-orcid' in app.extensions


def test_view(app):
    """Test view."""
    Babel(app)
    InvenioORCID(app)
    app.register_blueprint(blueprint)
    with app.test_client() as client:
        res = client.get("/")
        assert res.status_code == 200
        assert 'Welcome to Invenio-ORCID' in str(res.data)


def test_search(app):
    Babel(app)
    InvenioORCID(app)
    app.register_blueprint(blueprint)

    with app.test_client() as client:
        res = client.get("/search/name/eamonn")

        assert res.status_code == 200

        _result_json = json.loads(res.data)
        assert('orcid-search-results' in _result_json)
        assert(_result_json['orcid-search-results']['num-found'] > 0)

    with app.test_client() as client:
        res = client.get("/search/orcid/0000-0002-7277-7834")

        assert res.status_code == 200
        _result_json = json.loads(res.data)
        assert('orcid-search-results' in _result_json)
        assert(_result_json['orcid-search-results']['num-found'] == 1)


