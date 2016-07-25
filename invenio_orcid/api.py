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
"""ORCID search API."""

import requests
from flask import current_app
from requests.packages.urllib3.exceptions import HTTPError


def search(*args, **kwargs):
    """
    ORCID search endpoint.

    :param args:
    :param kwargs: e.g. type ='text', term ='Salvatore'
           or type= 'orcid', term= '0000-1221-1212-1231'
    :return: JSON response if success. Raises HTTPError if unsuccessful.
    """
    _headers = {'Content-Type': 'application/json'}
    _search_response = requests.get(
        current_app.config['ORCID_SEARCH_ENDPOINT'],
        {"q": "{type}:{term}".format(**kwargs)},
        headers=_headers)

    if _search_response.status_code != 200:
        raise HTTPError(
            "No response given from the ORCID endpoint at {0}".format(
                current_app.config['ORCID_SEARCH_ENDPOINT']))

    return _search_response.json()
