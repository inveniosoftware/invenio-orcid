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

"""Implement Celery tasks."""

from celery import shared_task
from celery.utils.log import get_task_logger
from flask import current_app
from invenio_db import db
from invenio_oauthclient.models import RemoteAccount, UserIdentity
from invenio_pidstore import current_pidstore
from invenio_pidstore.resolver import Resolver
from invenio_search.utils import schema_to_index
from requests import RequestException
from werkzeug.utils import import_string

from .models import ORCIDRecords
from .proxies import current_orcid
from .utils import get_authors_credentials

logger = get_task_logger(__name__)


def prepare_authors_data_for_pushing_to_orcid(data):
    """Extract the authors with valid ORCID credentials.

    It uses the list of authors from a given record in JSON format.
    """
    pid_type = current_app.config['ORCID_RECORDS_PID_TYPE']
    resolver = Resolver(pid_type=pid_type,
                        object_type='rec', getter=lambda x: x)
    fetcher_name = current_app.config['ORCID_RECORDS_PID_FETCHER']
    pid = current_pidstore.fetchers[fetcher_name](None, data)
    record_identifier = pid.pid_value
    record_id = resolver.resolve(record_identifier)[0].object_uuid
    authors = get_orcid_valid_authors(data)
    token = None
    author_orcid = ''
    authors_with_orcid_credentials = []
    for author in authors:
        try:
            token, author_orcid = get_authors_credentials(author)
        except AttributeError:
            continue
        try:
            authors_with_orcid_credentials.append((
                ORCIDRecords.query.filter_by(
                    orcid=author_orcid, record_id=record_id
                ).first().put_code,
                token, author_orcid, record_id
            ))
        except AttributeError:
            authors_with_orcid_credentials.append(
                ([], token, author_orcid, record_id))
            continue
    return authors_with_orcid_credentials


@shared_task(ignore_result=True)
def delete_from_orcid(sender, api=None):
    """Delete a record from orcid."""
    api = api or current_orcid.member
    pid_type = current_app.config['ORCID_RECORDS_PID_TYPE']
    resolver = Resolver(pid_type=pid_type,
                        object_type='rec', getter=lambda x: x)
    fetcher_name = current_app.config['ORCID_RECORDS_PID_FETCHER']
    pid = current_pidstore.fetchers[fetcher_name](None, sender)
    record_identifier = pid.pid_value
    record_id = resolver.resolve(record_identifier)[0].object_uuid
    records = ORCIDRecords.query.filter_by(record_id=record_id).all()
    for record in records:
        raw_user = UserIdentity.query.filter_by(
            id=record.orcid, method='orcid').first()
        user = RemoteAccount.query.filter_by(user_id=raw_user.id_user).first()
        token = user.remote_tokens[0].access_token
        api.remove_record(record.orcid, token, 'work', record.put_code)
        with db.session.begin_nested():
            db.session.delete(record)
        db.session.commit()


def doc_type_should_be_sent_to_orcid(record):
    """Return ``True`` is a document type should be sent to ORCID."""
    index, doc_type = schema_to_index(record['$schema'])
    main_doc_type = current_app.config['ORCID_RECORDS_DOC_TYPE']
    return doc_type == main_doc_type


@shared_task(ignore_result=True)
def send_to_orcid(sender, api=None):
    """Send records to orcid."""
    if doc_type_should_be_sent_to_orcid(sender):
        fetcher_name = current_app.config['ORCID_RECORDS_PID_FETCHER']
        pid = current_pidstore.fetchers[fetcher_name](None, sender)
        record_identifier = pid.pid_value
        current_app.logger.info('Sending "{0}" to orcid.'.format(
            record_identifier))
        try:
            api = api or current_orcid.member
            convert_to_orcid = import_string(
                current_app.config['ORCID_JSON_CONVERTER_MODULE'])
            orcid_json = convert_to_orcid(sender)
            authors = prepare_authors_data_for_pushing_to_orcid(sender)
            for author in authors:
                try:
                    put_code = author[0]
                    token = author[1]
                    author_orcid = author[2]
                    record_id = author[3]
                    if not put_code:
                        put_code = api.add_record(  # try-continue
                            author_orcid, token, 'work', orcid_json)
                        orcid_log_record = ORCIDRecords(
                            orcid=author_orcid,
                            record_id=record_id,
                            put_code=put_code)
                        with db.session.begin_nested():
                            db.session.add(orcid_log_record)
                        db.session.commit()
                    else:
                        api.update_record(author_orcid, token,
                                          'work', orcid_json, str(put_code))
                    current_app.logger.info(
                        'Succersfully sent "{0}" to orcid.'.format(
                            sender.get(record_identifier)))
                except RequestException as e:
                    current_app.logger.info(
                        e.response.text, sender[record_identifier])
                    current_app.logger.info(
                        'Failed to push "{0}" to orcid.'.format(
                            sender.get(record_identifier)))
                    continue
        except (KeyError, AttributeError, TypeError) as e:
            current_app.logger.info(
                'Failed to convert "{0}" to orcid.'.format(
                    sender.get(record_identifier)))


def get_author_collection_records_from_valid_authors(authors_refs):
    """Query elasticsearch for the author of the given authors references."""
    search_args = {
        'self__$ref': authors_refs
    }

    query = current_orcid.author_search().query('match', ids__type='ORCID') \
                                         .query('terms', **search_args)
    return query.execute().hits


def get_orcid_valid_authors(record):
    """Return all the valid author-records from a record.

    A valid author-rerord is one that contains an ORCID iD.
    """
    authors_refs = []
    for author in record['authors']:
        try:
            authors_refs.append(author['record']['$ref'])
        except KeyError:
            continue

    return get_author_collection_records_from_valid_authors(authors_refs)
