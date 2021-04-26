import logging

from datetime import datetime, timedelta
from getter.model.declarative import RawDocument
from requests.exceptions import HTTPError
from sickle import Sickle
from sickle.models import Record
from sickle.oaiexceptions import NoRecordsMatch
from urllib3.exceptions import MaxRetryError


class OAIAdapter:
    def __init__(self, collection):
        self.collection = collection
        self.source_name = '-'.join(['oai', collection])

    def get_raw(self, record: Record):
        raw_doc = RawDocument()

        raw_doc.gathering_date = datetime.utcnow()
        raw_doc.gathering_source = self.source_name
        raw_doc.code = record.header.identifier
        raw_doc.datestamp = datetime.strptime(record.header.datestamp, '%Y-%m-%d')
        raw_doc.set_specs = record.header.setSpecs

        data = {}
        for k in record.metadata.keys():
            data[k] = record.metadata.get(k, '')

        raw_doc.collection = self.collection
        raw_doc.data = data

        return raw_doc


class OAIClient:
    def __init__(self, collection, url, days_delta=30, max_retries=3):
        self.collection = collection
        self.source_name = '-'.join(['oai', self.collection])
        self.sickle = Sickle(url, max_retries=max_retries, verify=False)
        self.days_delta = days_delta

    def get_records(self, from_date='', until_date=''):
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            until_date = datetime.strptime(until_date, '%Y-%m-%d')
        except ValueError:
            until_date = datetime.now()
            from_date = until_date - timedelta(days=self.days_delta)

        try:
            records = self.sickle.ListRecords(**{'metadataPrefix': 'oai_dc',
                                                 'from': from_date.strftime('%Y-%m-%d'),
                                                 'until': until_date.strftime('%Y-%m-%d')})
        except NoRecordsMatch:
            logging.info('No records found')
            return []
        except (ConnectionError,
                ConnectionResetError,
                ConnectionAbortedError,
                ConnectionRefusedError,
                HTTPError,
                MaxRetryError,
                TimeoutError) as e:
            logging.error(e)
            return []

        return records
