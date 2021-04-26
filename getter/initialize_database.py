import logging
import os
import sys
sys.path.append(os.getcwd())

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from getter.model.declarative import Base


URI_RAW_DATA = os.environ.get('URI_RAW_DATA', 'postgresql://root:alemanha@172.17.0.3:5432/normalized')

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%b/%Y %H:%M:%S')


try:
    ENGINE = create_engine(URI_RAW_DATA)
    SESSION_FACTOTY = sessionmaker(bind=ENGINE)
    Base.metadata.create_all(ENGINE)

    logging.info('Database structure successfully created')
except (ConnectionError, ConnectionResetError, OperationalError) as e:
    logging.error(e)
