import argparse
import logging
import os

from datetime import datetime
from requests.exceptions import HTTPError
from util.database import upsert_raw
from util.oai_pmh import OAIClient, OAIAdapter
from util.values import COLLECTION_TO_URL, METADATA_PREFIXES
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URI_RAW_DATA = os.environ.get('URI_RAW_DATA', 'postgresql://postgres:alemanha@172.17.0.2:5432/normalized')

try:
    ENGINE = create_engine(URI_RAW_DATA)
    SESSION_FACTOTY = sessionmaker(bind=ENGINE)
except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as e:
    logging.error(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--collection', required=True, choices=COLLECTION_TO_URL.keys())
    parser.add_argument('-d', '--days_delta', default=30, type=int)
    parser.add_argument('-f', '--from_date', default='')
    parser.add_argument('-m', '--max_retries', default=3, type=int)
    parser.add_argument('-u', '--until_date', default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('-p', '--metadata_prefix', default='oai_dc_scielo', choices=METADATA_PREFIXES)
    parser.add_argument('-i', '--identifier')
    params = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s %(message)s', datefmt='%d/%b/%Y %H:%M:%S')

    oai_client = OAIClient(collection=params.collection, url=COLLECTION_TO_URL.get(params.collection), max_retries=params.max_retries, days_delta=params.days_delta)
    oai_adapter = OAIAdapter(collection=params.collection)

    session = SESSION_FACTOTY()
    try:
        if params.identifier:
            records = oai_client.get_record(metadata_prefix=params.metadata_prefix, identifier=params.identifier)
        else:
            records = oai_client.get_records(metadata_prefix=params.metadata_prefix, from_date=params.from_date, until_date=params.until_date)

        for record in records:
            raw_doc = oai_adapter.get_raw(record)
            upsert_raw(session, raw_doc)
    except HTTPError as e:
        logging.error(e)
    finally:
        session.close()


if __name__ == '__main__':
    main()
