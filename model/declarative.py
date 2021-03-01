from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON, INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RawDocument(Base):
    __tablename__ = 'raw_document'
    __table_args__ = (UniqueConstraint('gathering_source', 'collection', 'pid'), )

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    gathering_source = Column(VARCHAR(255), nullable=False)
    gathering_date = Column(TIMESTAMP, nullable=False)
    collection = Column(VARCHAR(255), nullable=False)
    pid = Column(VARCHAR(255), nullable=False)
    data = Column(JSON)


class NormJournal(Base):
    __tablename__ = 'norm_journal'

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    title = Column(VARCHAR(2048))
    abbreviated_title = Column(VARCHAR(512))
    print_issn = Column(VARCHAR(9))
    electronic_issn = Column(VARCHAR(9))


class NormDocument(Base):
    __tablename__ = 'norm_document'

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    publication_type = Column(VARCHAR(32))
    title = Column(VARCHAR(2048))
    year = Column(INTEGER)
    authors = Column(VARCHAR(2048))
    volume = Column(VARCHAR(64))
    start_page = Column(VARCHAR(64))

    fk_journal = Column(INTEGER, ForeignKey('norm_journal.id', name='norm_document_fk_journal_id'))
    fk_raw_document = Column(INTEGER, ForeignKey('raw_document.id', name='norm_document_fk_raw_document_id'))


class NormCitation(Base):
    __tablename__ = 'norm_citation'
    __table_args__ = (UniqueConstraint('fk_raw_document', 'number'),)

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    number = Column(INTEGER, nullable=False)
    publication_type = Column(VARCHAR(32))
    title = Column(VARCHAR(2048))
    year = Column(INTEGER)
    first_author = Column(VARCHAR(512))
    start_page = Column(VARCHAR(64))
    volume = Column(VARCHAR(64))

    fk_raw_document = Column(INTEGER, ForeignKey('raw_document.id', name='norm_citation_fk_raw_document_id'))
