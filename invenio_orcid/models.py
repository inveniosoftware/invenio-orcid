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
