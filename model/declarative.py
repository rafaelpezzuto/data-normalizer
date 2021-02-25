from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index, Date
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Journal(Base):
    __tablename__ = 'journal'
    __table_args__ = (UniqueConstraint('print_issn', 'online_issn', 'pid_issn', name='uni_journal_issn'),)
    __table_args__ += (Index('idx_print_issn', 'print_issn'),)
    __table_args__ += (Index('idx_online_issn', 'online_issn'),)
    __table_args__ += (Index('idx_pid_issn', 'pid_issn'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    print_issn = Column(VARCHAR(9), nullable=False)
    online_issn = Column(VARCHAR(9), nullable=False)
    pid_issn = Column(VARCHAR(9), nullable=False)

    # Todo: include other params


class Document(Base):
    __tablename__ = 'document'
    __table_args__ = (UniqueConstraint('collection_acronym', 'publisher_id', name='uni_document_col_pid'),)
    __table_args__ += (Index('idx_col_pid_jou', 'collection_acronym', 'publisher_id', 'fk_document_journal'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    collection_acronym = Column(VARCHAR(3), nullable=False)
    publisher_id = Column(VARCHAR(23), nullable=False)
    original_title = Column(VARCHAR(1024))
    first_author = Column(VARCHAR(255))
    document_publication_date = Column(VARCHAR(10))
    issue_publication_date = Column(VARCHAR(10))

    cl_title = Column(VARCHAR(1024))
    cl_first_author = Column(VARCHAR(255))
    cl_document_publication_date = Column(VARCHAR(10))
    cl_issue_publication_date = Column(VARCHAR(10))
    cl_publication_year = Column(VARCHAR(4))

    # Todo: include other params

    fk_document_journal = Column(INTEGER(unsigned=True), ForeignKey('journal.id', name='fk_document_journal'))
    journal = relationship(Journal)


class Citation(Base):
    __tablename__ = 'citation'
    __table_args__ = (UniqueConstraint('collection_acronym', 'publisher_id', 'index_number', name='uni_citation_col_pid_number'),)
    __table_args__ += (Index('idx_col_pid_number', 'collection_acronym', 'publisher_id', 'index_number'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    collection_acronym = Column(VARCHAR(3), nullable=False)
    publisher_id = Column(VARCHAR(23), nullable=False)
    index_number = Column(INTEGER(unsigned=True), nullable=False)

    # Todo: include other params

    fk_citation_document = Column(INTEGER(unsigned=True), ForeignKey('document.id', name='fk_citation_document'))
    document = relationship(Document)
