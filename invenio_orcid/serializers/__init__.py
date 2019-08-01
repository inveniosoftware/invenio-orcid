# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Record serialization."""

from __future__ import absolute_import, print_function

from .orcid_serializer import ORCIDSerializer

from invenio_records_rest.serializers.response import record_responsify, \
                                                      search_responsify

orcid = ORCIDSerializer()

orcid_response = record_responsify(orcid, 'application/x-orcid')

orcid_search = search_responsify(orcid, 'application/x-orcid')
