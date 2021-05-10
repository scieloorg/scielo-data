import argparse
import logging
import os

from datetime import datetime
from getter.lib.database import upsert_raw
from getter.lib.oai_pmh import OAIClient, OAIAdapter
from getter.lib.values import COLLECTION_TO_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URI_RAW_DATA = os.environ.get('URI_RAW_DATA', 'postgresql://root:alemanha@172.17.0.2:5432/normalized')

try:
    ENGINE = create_engine(URI_RAW_DATA)
    SESSION_FACTOTY = sessionmaker(bind=ENGINE)
except (ConnectionError,
        ConnectionResetError,
        ConnectionAbortedError,
        ConnectionRefusedError) as e:
    logging.error(e)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--collection', required=True, choices=COLLECTION_TO_URL.keys())
    parser.add_argument('-d', '--days_delta', default=30, type=int)
    parser.add_argument('-f', '--from_date', default='')
    parser.add_argument('-m', '--max_retries', default=3, type=int)
    parser.add_argument('-u', '--until_date', default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('-p', '--metadata_prefix', default='oai_dc_scielo')

    params = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname)s %(message)s',
                        datefmt='%d/%b/%Y %H:%M:%S')

    oai_client = OAIClient(collection=params.collection,
                           url=COLLECTION_TO_URL.get(params.collection),
                           max_retries=params.max_retries,
                           days_delta=params.days_delta)
    oai_adapter = OAIAdapter(collection=params.collection)

    logging.info('Sending requests to %s' % COLLECTION_TO_URL.get(params.collection))
    records = oai_client.get_records(metadata_prefix=params.metadata_prefix,
                                     from_date=params.from_date,
                                     until_date=params.until_date)

    raw_documents = map(oai_adapter.get_raw, records)

    session = SESSION_FACTOTY()
    for rd in raw_documents:
        upsert_raw(session, rd)
    session.close()


if __name__ == '__main__':
    run()
