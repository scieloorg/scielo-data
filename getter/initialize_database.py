import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from model.declarative import Base


URI_RAW_DATA = os.environ.get('URI_RAW_DATA', 'postgresql://root:alemanha@172.17.0.3:5432/normalized')
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s %(message)s', datefmt='%d/%b/%Y %H:%M:%S')


def main():
    try:
        ENGINE = create_engine(URI_RAW_DATA)
        Base.metadata.create_all(ENGINE)

        logging.info('Database structure successfully created')
    except (ConnectionError, ConnectionResetError, OperationalError) as e:
        logging.error(e)
