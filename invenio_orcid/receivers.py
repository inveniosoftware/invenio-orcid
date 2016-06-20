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

"""Implement signal handlers."""

from invenio_records.signals import before_record_delete

from .tasks import delete_from_orcid, send_to_orcid


def send_records_to_orcid(sender, record, **kwargs):
    """Schedule a Celery task that sends every new/updated record to ORCID.

    :param sender: Flask application.
    :param record: The record to be sent to ORCID in JSON format.
    """
    send_to_orcid.delay(record)


def delete_record_from_orcid(sender, record, **kwargs):
    """Schedule a Celery task that removes records from ORCID.

    :param sender: Flask application.
    :param record: The record to be sent to ORCID in JSON format.
    """
    delete_from_orcid.delay(sender=sender)
