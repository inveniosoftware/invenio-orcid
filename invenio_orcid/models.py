# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Define models for storing relations between ORCID and records."""

from invenio_db import db
from sqlalchemy_utils.types import UUIDType


class ORCIDRecords(db.Model):
    """Store links between records and ORCIDs."""

    __tablename__ = 'orcid_records'

    orcid = db.Column(db.String(160), primary_key=True)
    record_id = db.Column(UUIDType)
    # TODO add foreign key or reference to PIDStore
    put_code = db.Column(db.Integer, primary_key=True)
