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

"""Implement helper functions."""

from invenio_oauthclient.models import RemoteAccount, UserIdentity


def get_authors_credentials(author_identifier, method='orcid'):
    """Return the access token for a specific author (if available).

    :param author_identifier: The id of the author (e.g. the orcid-id).
    :param method: The service associated with the author_identifier.
    """
    raw_user = UserIdentity.query.filter_by(
        id=author_identifier, method=method).first()
    user = RemoteAccount.query.filter_by(user_id=raw_user.id_user).first()
    return user.tokens[0].access_token


def convert_to_orcid(record):
    """Dummy converter, assuming that the record is a dojson serialization of MARC.

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
