from sqlalchemy import Column, VARCHAR, UniqueConstraint, INTEGER, DATE
from sqlalchemy.dialects.postgresql import JSON, TIMESTAMP, ARRAY
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RawDocument(Base):
    __tablename__ = 'raw_document'
    __table_args__ = (UniqueConstraint('gathering_source', 'collection', 'code'), )

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    gathering_source = Column(VARCHAR(255), nullable=False)
    gathering_date = Column(TIMESTAMP, nullable=False)
    collection = Column(VARCHAR(255), nullable=False)
    code = Column(VARCHAR(255), nullable=False)
    datestamp = Column(TIMESTAMP, nullable=False)
    set_specs = Column(ARRAY(VARCHAR(255)), nullable=False)
    data = Column(JSON)


class NormJournal(Base):
    __tablename__ = 'norm_journal'

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    issn = Column(ARRAY(VARCHAR))
    e_issn = Column(ARRAY(VARCHAR))
    title = Column(VARCHAR(255))
    abbreviated_title = Column(VARCHAR(255))
    alternative_titles = Column(ARRAY(VARCHAR))
    # country = Column(VARCHAR)
    # creation_date = Column(DATE)
    # ceassing_date = Column(DATE)
    # publisher = Column(VARCHAR)
    # publisher_address = Column(VARCHAR)


class NormDocument(Base):
    __tablename__ = 'norm_document'

    id = Column(INTEGER, primary_key=True, autoincrement=True)

