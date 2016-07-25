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

"""ORCID integration for Invenio."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, render_template
from flask_babelex import gettext as _
from functools import wraps
from requests import HTTPError

from invenio_orcid.api import search as orcid_search

blueprint = Blueprint(
    'invenio_orcid',
    __name__,
    url_prefix='/orcid',
    template_folder='templates',
    static_folder='static',
)


def orcid_http_error_wrapper(fn):
    def http_call_wrap(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except HTTPError, http_error:
            return jsonify({'error': http_error.args})
        except Exception, e:
            return jsonify(
                {'error': 'Unable to connect to ORCID endpoint: {0}'
                    .format(e.args)})
    return wraps(fn)(http_call_wrap)


@blueprint.route('/')
def index():
    """Basic view."""
    return render_template(
        'invenio_orcid/index.html',
        module_name=_('Invenio-ORCID'))


@blueprint.route('/search/name/<string:name>')
@orcid_http_error_wrapper
def search_string(name):
    """
    Search the ORCID endpoint for people with a given name.

    :param name: String representing the name to be searched on
    :return: JSON representing the search results
    """

    result = orcid_search(type='text', term=name)
    return jsonify(result)


@blueprint.route('/search/orcid/<string:orcid>')
@orcid_http_error_wrapper
def search_orcid(orcid):
    """
    Search the ORCID endpoint for people with a given ORCID iD.

    :param name: String representing the ORCID iD to be searched on
    :return: JSON representing the search results
    """
    result = orcid_search(type='orcid', term=orcid)
    return jsonify(result)

