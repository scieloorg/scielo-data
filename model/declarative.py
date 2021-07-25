from sqlalchemy import Column, VARCHAR, UniqueConstraint, INTEGER
from sqlalchemy.dialects.postgresql import JSON, TIMESTAMP, ARRAY
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RawDocument(Base):
    __tablename__ = 'raw_document'
    __table_args__ = (UniqueConstraint('gathering_source', 'collection', 'identifier'), )

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    gathering_source = Column(VARCHAR(255), nullable=False)
    gathering_date = Column(TIMESTAMP, nullable=False)
    collection = Column(VARCHAR(255), nullable=False)
    identifier = Column(VARCHAR(255), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    is_part_of = Column(ARRAY(VARCHAR(255)), nullable=False)
    data = Column(JSON)
