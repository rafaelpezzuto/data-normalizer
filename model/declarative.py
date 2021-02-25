from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index
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
    __table_args__ = (UniqueConstraint('collection', 'pid', name='uni_document_col_pid'),)
    __table_args__ += (Index('idx_col_pid_jou', 'collection', 'pid', 'fk_document_journal'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    collection = Column(VARCHAR(3), nullable=False)
    pid = Column(VARCHAR(23), nullable=False)
    title = Column(VARCHAR(255))
    first_author = Column(VARCHAR(255))

    cl_title = Column(VARCHAR(255))
    cl_first_author = Column(VARCHAR(255))

    # Todo: include other params

    fk_document_journal = Column(INTEGER(unsigned=True), ForeignKey('journal.id', name='fk_document_journal'))
    journal = relationship(Journal)


class Citation(Base):
    __tablename__ = 'citation'
    __table_args__ = (UniqueConstraint('collection', 'pid', 'number', name='uni_citation_col_pid_number'),)
    __table_args__ += (Index('idx_col_pid_number', 'collection', 'pid', 'number'),)

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    collection = Column(VARCHAR(3), nullable=False)
    pid = Column(VARCHAR(23), nullable=False)
    number = Column(INTEGER(unsigned=True), nullable=False)

    # Todo: include other params

    fk_citation_document = Column(INTEGER(unsigned=True), ForeignKey('document.id', name='fk_citation_document'))
    document = relationship(Document)
