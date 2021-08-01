import logging

from datetime import datetime, timedelta
from model.oai_dc_scielo import SciELORecord
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch
from urllib3.exceptions import MaxRetryError


class OAIClient:
    def __init__(self, url, source_name, days_delta=30, max_retries=3):
        self.sickle = Sickle(url, max_retries=max_retries, verify=False)
        self.sickle.class_mapping['ListRecords'] = SciELORecord
        self.sickle.class_mapping['GetRecord'] = SciELORecord
        self.days_delta = days_delta
        self.source_name = source_name

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

    def record_to_dict(self, record: SciELORecord):
        object = {}

        object['gathering_date'] = datetime.utcnow()
        object['gathering_source'] = self.source_name
        object['identifier'] = record.header.identifier
        object['date'] = record.header.date
        object['is_part_of'] = record.header.is_part_of
        object['metadata'] = record.get_metadata().get('metadata', {})

        return object
