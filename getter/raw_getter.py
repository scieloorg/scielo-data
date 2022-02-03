import argparse
import logging
import os

from datetime import datetime, timedelta
from util import exceptions, storage_impl, oai_pmh, values


LOGGING = os.environ.get('SCIELO_NW_LOGGING_LEVEL', 'INFO')
BULK_SIZE = int(os.environ.get('SCIELO_NW_BULK_SIZE', '10'))
OAI_ADDRESS = os.environ.get('SCIELO_NW_OAI_ADDRESS', 'https://old.scielo.br/oai/scielo-oai.php')
SOURCE_NAME = os.environ.get('SCIELO_NW_SOURCE_NAME', 'oai-scl')
DB_CONNECTION = os.environ.get('SCIELO_NW_DB_CONNECTION', '')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--oai_address', default=OAI_ADDRESS, help='Endereço do site do Provedor OAI-PMH (e.g. https://old.scielo.br/oai/scielo-oai.php)')
    parser.add_argument('-n', '--source_name', default=SOURCE_NAME, help='Nome da fonte de dados (e.g. oai-old-scl)')
    parser.add_argument('-p', '--metadata_prefix', default='oai_dc', choices=values.METADATA_PREFIXES, help='Prefixo de metadados')
    parser.add_argument('-m', '--max_retries', default=3, type=int, help='Número máximo de tentativas de coleta no Provedor OAI-PMH')
    parser.add_argument('-i', '--identifier', help='Código de documento (formato oai:scielo:<PID>)')

    parser.add_argument(
        '-f', 
        '--from_date',
        default=(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
        help='Data de processamento até a qual os dados serão considerados para coleta (formato YYYY-MM-DD)',
    )

    parser.add_argument(
        '-u', 
        '--until_date', 
        default=datetime.now().strftime('%Y-%m-%d'),
        help='Data de processamento a partir da qual os dados serão coletados (formato YYYY-MM-DD)',
    )

    parser.add_argument(
        '-l',
        '--logging_level',
        default=LOGGING,
        choices=['INFO', 'WARNING', 'DEBUG'],
        help='Modo de logging'),

    parser.add_argument(
        '--storage_mode',
        choices=['database', 'json'],
        default='json',
        help='Modo de persistência dos dados coletados',
    )
    
    parser.add_argument(
        '--db_connection',
        default=DB_CONNECTION,
        help='Uma string de conexão com banco de dados',
    )

    parser.add_argument(
        '--output',
        default='.'.join(['obtained', datetime.utcnow().strftime('%Y-%m-%d.%H%M%S%f'), 'json']),
        help='Um caminho no disco em que os dados serão armazenados',
    )

    params = parser.parse_args()

    logging.basicConfig(level=params.logging_level, format='[%(asctime)s] %(levelname)s %(message)s', datefmt='%d/%b/%Y %H:%M:%S')

    oai_client = oai_pmh.OAIClient(url=params.oai_address, metadata_prefix=params.metadata_prefix, source_name=params.source_name, max_retries=params.max_retries)
  
    if params.storage_mode == 'database':
        # instancia client em modo de banco de dados
        if not params.db_connection:
            raise exceptions.DatabaseConnectionUndefinedError("String de conexão de banco de dados indefinida.")
        raw_client = storage_impl.StorageClientDatabase()
        raw_client.open(params.db_connection)

    elif params.storage_mode == 'json':
        # instancia client em modo de arquivo
        raw_client = storage_impl.StorageClientFile()
        raw_client.open(params.output)

    if params.identifier:
        records = oai_client.get_record(identifier=params.identifier)
    else:
        records = oai_client.get_records(from_date=params.from_date, until_date=params.until_date)

    objects = []

    for r in records:
        objects.append(oai_client.record_to_dict(r))

        if len(objects) == BULK_SIZE:
            raw_client.save(objects)
            objects = []

    if objects:
        raw_client.save(objects)
    raw_client.close()
