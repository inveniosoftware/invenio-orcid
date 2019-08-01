# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Implement helper functions."""

from flask import current_app
from invenio_oauthclient.models import RemoteAccount, UserIdentity
from werkzeug.utils import import_string


def get_authors_credentials(author, method='orcid'):
    """Return the access token for a specific author (if available).

    :param author: An author record.
    :param method: The service associated with the author_identifier.
    """
    get_identifier = import_string(
        current_app.config['ORCID_ID_FETCHER'])
    author_identifier = get_identifier(author)
    raw_user = UserIdentity.query.filter_by(
        id=author_identifier, method=method).first()
    user = RemoteAccount.query.filter_by(user_id=raw_user.id_user).first()

    return user.remote_tokens[0].access_token, author_identifier


def get_orcid_id(author):
    """Return the ORCID ID of a given author record.

    :param author: An author record.
    """
    return author['orcid']


def convert_to_orcid(record):
    """Create orcid using a dummy converter.

    The converter assumes that the record is a dojson serialization of MARC.
    To create yours see https://github.com/ORCID/python-orcid
    and http://members.orcid.org/api.
    """
    return {
        "title": {
            "title": record[0]['title_statement']['title']
        },
        "type": "JOURNAL_ARTICLE",
        "external-ids": {
            "external-id": [
                {
                    "external-id-value": record[0]['other_standard_identifier']
                    ['standard_number_or_code'],
                    "external-id-type": "doi",
                    "external-id-relationship": "SELF"
                }
            ]
        }
    }
