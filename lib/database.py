from model.declarative import Base, Document
from pymongo import MongoClient
from pymongo.uri_parser import parse_uri
from sqlalchemy import create_engine
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


def export_document(database_uri, document_attrs):
    doc = Document()
    doc.collection = document_attrs['collection']
    doc.pid = document_attrs['pid']
    doc.title = document_attrs['original_title']
    doc.first_author = document_attrs['first_author']

    doc.cl_title = document_attrs['cl_title']
    doc.cl_first_author = document_attrs['cl_first_author']

    session = get_session(database_uri)
    session.add(doc)
    session.commit()


def export_citation(database_uri, citation_attrs):
    pass