import argparse
import logging
import os

from sqlalchemy.exc import IntegrityError

from clients.oai_pmh import get_records, record_to_raw_doc
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.declarative import RawDocument


URI_RAW_DATA = os.environ.get('URI_RAW_DATA', 'postgresql://postgres:alemanha@172.17.0.6:5432/normalized')
ENGINE = create_engine(URI_RAW_DATA)
SESSION_FACTOTY = sessionmaker(bind=ENGINE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from_date', default='')
    parser.add_argument('-u', '--until_date', default=datetime.now().strftime('%Y-%m-%d'))

    params = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname)s %(message)s',
                        datefmt='%d/%b/%Y %H:%M:%S')

    records = get_records(from_date=params.from_date, until_date=params.until_date)
    raw_documents = map(record_to_raw_doc, records)

    session = SESSION_FACTOTY()

    for rd in raw_documents:
        try:
            session.add(rd)
            session.commit()
            logging.info('Saved %s' % rd.code)
        except IntegrityError:
            session.rollback()
            existing_record = session.query(RawDocument).filter(RawDocument.gathering_source == rd.gathering_source,
                                                                RawDocument.collection == rd.collection,
                                                                RawDocument.code == rd.code).one()
            if existing_record.datestamp < rd.datestamp:
                session.delete(existing_record)
                session.flush()
                session.add(rd)
                session.commit()
                logging.info('Updated %s' % rd.code)

    session.close()
