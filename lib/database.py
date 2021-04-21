import logging

from bson import json_util
from model.declarative import Base, RawDocument, NormDocument, NormCitation
from pymongo import MongoClient
from pymongo.uri_parser import parse_uri
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy_utils import database_exists, create_database


def mongo_collection(mongo_uri):
    parsed_uri = parse_uri(mongo_uri)

    database = parsed_uri['database']
    collection = parsed_uri['collection']

    return MongoClient(mongo_uri).get_database(database).get_collection(collection)


def create_tables(database_uri):
    if not database_exists(database_uri):
        create_database(database_uri)

    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)


def export_journal(database_uri, journal_attrs):
    pass


def export_data(session, docs):
    for doc_attrs in docs:
        raw_d = RawDocument()

        for a in ['gathering_source',
                  'gathering_date',
                  'collection',
                  'pid']:
            raw_d.__setattr__(a, doc_attrs[a])
        raw_d.data = json_util.dumps(doc_attrs['data'])

        norm_d = NormDocument()
        for k, v in doc_attrs['norm_doc'].items():
            norm_d.__setattr__(k, v)

        citations = []
        for cit in doc_attrs['norm_cits']:
            norm_c = NormCitation()
            for k, v in cit.items():
                norm_c.__setattr__(k, v)
            citations.append(norm_c)

        try:
            session.add(raw_d)
            session.add(norm_d)
            session.add_all(citations)
            session.commit()
        except IntegrityError as ie:
            logging.error(ie)
            session.rollback()
        except DataError as de:
            logging.error(de)
            session.rollback()
        except UnicodeEncodeError as uee:
            logging.error(uee)
            session.rollback()
