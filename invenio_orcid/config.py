# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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
ORCID_RECORDS_DOC_TYPES = {'records', }
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
