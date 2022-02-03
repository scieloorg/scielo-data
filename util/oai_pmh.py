import logging

from datetime import datetime
from model.oai_dc_scielo import SciELORecord
from sickle import oaiexceptions, Sickle
from util import exceptions, values


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
            raise exceptions.InvalidDateFormatError('Formato de datas inválido.')

        if from_date >= until_date:
            raise exceptions.InvalidDateRangeError('Data de início é maior ou igual a data de fim.')

        logging.info(f'Obtendo dados do período de {from_date.strftime("%Y-%m-%d")} a {until_date.strftime("%Y-%m-%d")}')

        try:
            return self.sickle.ListRecords(
                **{
                    'metadataPrefix': self.metadata_prefix, 
                    'from': from_date.strftime('%Y-%m-%d'), 
                    'until': until_date.strftime('%Y-%m-%d')
                }
            )
        
        except oaiexceptions.CannotDisseminateFormat:
            logging.error(f'Prefixo de metadados {self.metadata_prefix} inexistente no provedor {self.url}.')
        
        except oaiexceptions.NoRecordsMatch:
            logging.info('Não foram encontrados registros.')

    def record_to_dict(self, record):
        parsed_record = {}

        parsed_record['gathering_date'] = datetime.utcnow()
        parsed_record['gathering_source'] = self.source_name
        parsed_record['identifier'] = record.header.identifier

        self._parse_header(record.header, parsed_record)
        self._parse_metadata(record.metadata, parsed_record)

        return parsed_record

    def _parse_header(self, header, parsed_record):
        if self.metadata_prefix == values.OAI_DC:
            parsed_record['date'] = header.datestamp
            parsed_record['is_part_of'] = header.setSpecs

        elif self.metadata_prefix == values.OAI_DC_SCIELO:
            parsed_record['date'] = header.date
            parsed_record['is_part_of'] = header.is_part_of        

    def _parse_metadata(self, metadata, parsed_record):
        if self.metadata_prefix == values.OAI_DC:
            parsed_record['metadata'] = metadata

        elif self.metadata_prefix == values.OAI_DC_SCIELO:
            parsed_record['metadata'] = metadata.get('metadata', {})
