import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.declarative import Base


URI_RAW_DATA = os.environ.get('URI_RAW_DATA', 'postgresql://postgres:alemanha@172.17.0.6:5432/normalized')
ENGINE = create_engine(URI_RAW_DATA)
SESSION_FACTOTY = sessionmaker(bind=ENGINE)

Base.metadata.create_all(ENGINE)
