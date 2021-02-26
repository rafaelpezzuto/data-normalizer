from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index, TEXT
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from lib.values import (
    ARTICLEMETA_DOCUMENT_STR_FIELDS,
    ARTICLEMETA_DOCUMENT_CLEANED_FIELDS,
    ARTICLEMETA_DOCUMENT_METHOD_FIELDS
)

Base = declarative_base()


class Journal(Base):
    __tablename__ = 'journal'
    __table_args__ = (UniqueConstraint('print_issn', 'electronic_issn', name='uni_journal_issn'),)
    __table_args__ += (Index('idx_print_issn', 'print_issn'),)
    __table_args__ += (Index('idx_electronic_issn', 'electronic_issn'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    print_issn = Column(VARCHAR(9))
    electronic_issn = Column(VARCHAR(9))
    acronym = Column(VARCHAR(10))
    title = Column(VARCHAR(255))
    abbreviated_title = Column(VARCHAR(255))
    publisher_name = Column(VARCHAR(255))


class Document(Base):
    __tablename__ = 'document'
    __table_args__ = (UniqueConstraint('collection_acronym', 'publisher_id', name='uni_document_col_pid'),)
    __table_args__ += (Index('idx_col_pid_jou', 'collection_acronym', 'publisher_id', 'fk_document_journal'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)

    for k, n in ARTICLEMETA_DOCUMENT_STR_FIELDS.items():
        exec('%s = Column(VARCHAR(%d))' % (k, n))

        if k in ARTICLEMETA_DOCUMENT_CLEANED_FIELDS:
            exec('cl_%s = Column(VARCHAR(%d))' % (k, n))

    for k, n in ARTICLEMETA_DOCUMENT_METHOD_FIELDS.items():
        exec('%s = Column(VARCHAR(%d))' % (k, n))

        if k in ARTICLEMETA_DOCUMENT_CLEANED_FIELDS:
            exec('cl_%s = Column(VARCHAR(%d))' % (k, n))

    original_abstracts = Column(TEXT)
    translated_abstracts = Column(TEXT)

    fk_document_journal = Column(INTEGER(unsigned=True), ForeignKey('journal.id', name='fk_document_journal'))
    journal = relationship(Journal)


class Citation(Base):
    __tablename__ = 'citation'
    __table_args__ = (
    UniqueConstraint('collection_acronym', 'publisher_id', 'index_number', name='uni_citation_col_pid_number'),)
    __table_args__ += (Index('idx_col_pid_number', 'collection_acronym', 'publisher_id', 'index_number'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    collection_acronym = Column(VARCHAR(3), nullable=False)
    publisher_id = Column(VARCHAR(23), nullable=False)
    index_number = Column(INTEGER(unsigned=True), nullable=False)

    # Todo: include other params

    fk_citation_document = Column(INTEGER(unsigned=True), ForeignKey('document.id', name='fk_citation_document'))
    document = relationship(Document)
