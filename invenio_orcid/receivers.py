# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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
