import logging
import os

from datetime import datetime, timedelta
from model.declarative import RawDocument
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch
from values import COLLECTION_TO_URL


COLLECTION_ACRONYM = os.environ.get('COLLECTION', 'scl')
RAW_OAI_PMH = '-'.join(['oai', COLLECTION_ACRONYM])


def record_to_raw_doc(record):
    raw_doc = RawDocument()

    raw_doc.gathering_date = datetime.utcnow()
    raw_doc.gathering_source = RAW_OAI_PMH
    raw_doc.code = record.header.identifier
    raw_doc.datestamp = datetime.strptime(record.header.datestamp, '%Y-%m-%d')
    raw_doc.set_specs = record.header.setSpecs

    data = {}
    for k in record.metadata.keys():
        data[k] = record.metadata.get(k, '')

    raw_doc.collection = COLLECTION_ACRONYM
    raw_doc.data = data

    return raw_doc


def get_records(from_date='', until_date=''):
    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        until_date = datetime.strptime(until_date, '%Y-%m-%d')
    except ValueError:
        until_date = datetime.now()
        from_date = until_date - timedelta(days=30)

    sik = Sickle(COLLECTION_TO_URL[COLLECTION_ACRONYM], verify=False)

    try:
        records = sik.ListRecords(**{'metadataPrefix': 'oai_dc',
                                     'from': from_date.strftime('%Y-%m-%d'),
                                     'until': until_date.strftime('%Y-%m-%d')})
    except NoRecordsMatch:
        logging.info('Não foram localizados registros')
        return []

    return records
