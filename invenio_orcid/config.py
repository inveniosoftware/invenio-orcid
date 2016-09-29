# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Default configuration for ORCID integration."""

from __future__ import absolute_import

ORCID_SYNCHRONIZATION_ENABLED = True

ORCID_RECORD_SERIALIZER = {
    'application/x-orcid': ('.serializers:orcid_response'),
}

ORCID_JSON_CONVERTER_MODULE = 'invenio_orcid.utils:convert_to_orcid'
ORCID_ID_FETCHER = 'invenio_orcid.utils:get_orcid_id'

ORCID_AUTHORS_SEARCH_CLASS = 'invenio_search:RecordsSearch'

ORCID_RECORDS_PID_TYPE = 'records'
ORCID_RECORDS_DOC_TYPE = 'records'
ORCID_RECORDS_PID_FETCHER = 'recid_fetcher'

ORCID_WORK_TYPES = {}
"""Mapping to ORCID work types.

Example:

.. code-block:: python

    ORCID_WORK_TYPES = {
        'conferencepaper': 'CONFERENCE_PAPER',
        'proceedings': 'BOOK',
    }
"""
