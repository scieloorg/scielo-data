import logging

from datetime import datetime, timedelta
from util.values import COLLECTION_TO_DATESTAMP_FORMAT
from model.declarative import RawDocument
from model.oai_dc_scielo import SciELORecord
from sickle import Sickle
from sickle.models import Record
from sickle.oaiexceptions import NoRecordsMatch
from urllib3.exceptions import MaxRetryError


class OAIClient:
    def __init__(self, collection, url, days_delta=30, max_retries=3):
        self.collection = collection
        self.source_name = '-'.join(['oai', self.collection])
        self.sickle = Sickle(url, max_retries=max_retries, verify=False)
        self.sickle.class_mapping['ListRecords'] = SciELORecord
        self.sickle.class_mapping['GetRecord'] = SciELORecord
        self.days_delta = days_delta

    def get_record(self, metadata_prefix='oai_dc_scielo', identifier=None):
        if identifier:
            return [self.sickle.GetRecord(**{'metadataPrefix': metadata_prefix, 'identifier': identifier})]

    def get_records(self, metadata_prefix='oai_dc_scielo', from_date='', until_date=''):
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            until_date = datetime.strptime(until_date, '%Y-%m-%d')
        except ValueError:
            until_date = datetime.now()
            from_date = until_date - timedelta(days=self.days_delta)

        try:
            records = self.sickle.ListRecords(**{'metadataPrefix': metadata_prefix, 'from': from_date.strftime('%Y-%m-%d'), 'until': until_date.strftime('%Y-%m-%d')})
        except NoRecordsMatch:
            logging.info('No records found')
            return []
        except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, MaxRetryError, TimeoutError) as e:
            logging.error(e)
            return []

        return records
