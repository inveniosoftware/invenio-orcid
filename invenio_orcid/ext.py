# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""ORCID integration for Invenio."""

from __future__ import absolute_import, print_function

import orcid
import six
from werkzeug.utils import cached_property, import_string

from . import config


class _ORCIDState(object):
    """ORCID state for an API access."""

    def __init__(self, app):
        """Initialize state."""
        self.app = app

        if app.config['ORCID_SYNCHRONIZATION_ENABLED']:
            # TODO register signal handlers
            # from .handlers import ...
            # handler.connect_via(app)
            pass

    @cached_property
    def member(self):
        orcid_base_url = self.app.config['OAUTHCLIENT_REMOTE_APPS'][
            'orcid']['params']['base_url']
        orcid_consumer_secret = self.app.config[
            'OAUTHCLIENT_ORCID_CREDENTIALS']['consumer_secret']
        orcid_consumer_key = self.app.config[
            'OAUTHCLIENT_ORCID_CREDENTIALS']['consumer_key']
        sandbox = (orcid_base_url == 'https://pub.sandbox.orcid.org/')

        return orcid.MemberAPI(
            orcid_consumer_secret, orcid_consumer_key, sandbox=sandbox
        )

    @cached_property
    def author_search(self):
        """Return a cache instance."""
        author_search = self.app.config.get('ORCID_AUTHORS_SEARCH_CLASS')

        return import_string(author_search) \
            if isinstance(author_search, six.string_types) \
            else author_search


class InvenioORCID(object):
    """Invenio-ORCID extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self._state = self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['invenio-orcid'] = _ORCIDState(app)

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault(
            'ORCID_BASE_TEMPLATE',
            app.config.get('BASE_TEMPLATE',
                           'invenio_orcid/base.html'))
        for k in dir(config):
            if k.startswith('ORCID_'):
                app.config.setdefault(k, getattr(config, k))

    def __getattr__(self, name):
        """Proxy to state object."""
        return getattr(self._state, name, None)
