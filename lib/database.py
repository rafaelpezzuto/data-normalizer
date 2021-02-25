import logging

from model.declarative import Base, Document
from pymongo import MongoClient
from pymongo.uri_parser import parse_uri
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
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


def get_session(database_uri):
    engine = create_engine(database_uri)
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    return db_session()


def export_journal(database_uri, journal_attrs):
    pass


def export_documents(database_uri, documents_attrs):
    session = get_session(database_uri)

    for dattrs in documents_attrs:
        doc = Document()
        doc.collection_acronym = dattrs['collection_acronym']
        doc.publisher_id = dattrs['publisher_id']
        doc.original_title = dattrs['original_title']
        doc.first_author = dattrs['first_author']
        doc.document_publication_date = dattrs['document_publication_date']
        doc.issue_publication_date = dattrs['issue_publication_date']

        doc.cl_title = dattrs['cl_title']
        doc.cl_first_author = dattrs['cl_first_author']
        doc.cl_document_publication_date = dattrs['cl_document_publication_date']
        doc.cl_issue_publication_date = dattrs['cl_issue_publication_date']
        doc.cl_publication_year = dattrs['cl_publication_year']

        try:
            session.add(doc)
            session.commit()
        except IntegrityError as ie:
            logging.error(ie)
            session.rollback()
        except UnicodeEncodeError as uee:
            logging.error(uee)
            session.rollback()


def export_citation(database_uri, citation_attrs):
    pass
