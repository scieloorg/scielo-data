import logging

from datetime import datetime, timedelta
from model.oai_dc_scielo import SciELORecord
from sickle import Sickle
from sickle.oaiexceptions import NoRecordsMatch
from util import exceptions
from urllib3.exceptions import MaxRetryError
from requests.exceptions import HTTPError


class OAIClient:
    def __init__(self, url, source_name, metadata_prefix=values.OAI_DC, max_retries=3):
        self.url = url
        self.sickle = Sickle(url, max_retries=max_retries, verify=False)
        self.metadata_prefix = metadata_prefix

        if self.metadata_prefix == values.OAI_DC_SCIELO:
            self.sickle.class_mapping['ListRecords'] = SciELORecord
            self.sickle.class_mapping['GetRecord'] = SciELORecord
        
        self.source_name = source_name

    def get_record(self, identifier=None):
        if identifier:
            return [self.sickle.GetRecord(**{'metadataPrefix': self.metadata_prefix, 'identifier': identifier})]

    def get_records(self, from_date='', until_date=''):
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            until_date = datetime.strptime(until_date, '%Y-%m-%d')
        except ValueError:
            raise exceptions.InvalidDateFormatError('Formato de datas inválido')

        if from_date >= until_date:
            raise exceptions.InvalidDateRangeError('Data de início é maior ou igual a data de fim')

        logging.info(f'Collecting data from {from_date.strftime("%Y-%m-%d")} to {until_date.strftime("%Y-%m-%d")}')

        try:
            records = self.sickle.ListRecords(**{'metadataPrefix': metadata_prefix, 'from': from_date.strftime('%Y-%m-%d'), 'until': until_date.strftime('%Y-%m-%d')})
        except NoRecordsMatch:
            logging.info('No records found')
            return []
        except (
            ConnectionError, 
            ConnectionResetError, 
            ConnectionAbortedError, 
            ConnectionRefusedError, 
            MaxRetryError, 
            HTTPError,
            TimeoutError,
        ) as e:
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
