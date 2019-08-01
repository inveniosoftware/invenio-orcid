# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Module tests."""

from __future__ import absolute_import, print_function

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
