import argparse
import logging
import os

from datetime import datetime
from util.storage_impl import (
    StorageClientDatabase,
    StorageClientFile,
)
from util.oai_pmh import OAIClient
from util.values import METADATA_PREFIXES


LOGGING = os.environ.get('SCIELO_NW_LOGGING_LEVEL', 'INFO')
BULK_SIZE = int(os.environ.get('SCIELO_NW_BULK_SIZE', '10'))
OAI_ADDRESS = os.environ.get('SCIELO_NW_OAI_ADDRESS', 'https://old.scielo.br/oai/scielo-oai.php')
SOURCE_NAME = os.environ.get('SCIELO_NW_SOURCE_NAME', 'oai-old-scl')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--oai_address', default=OAI_ADDRESS, help='Endereço do site do Provedor OAI-PMH (e.g. https://old.scielo.br/oai/scielo-oai.php)')
    parser.add_argument('-n', '--source_name', default=SOURCE_NAME, help='Nome da fonte de dados (e.g. oai-old-scl)')
    parser.add_argument('-p', '--metadata_prefix', default='oai_dc_scielo', choices=METADATA_PREFIXES, help='Prefixo de metadados')
    parser.add_argument('-m', '--max_retries', default=3, type=int, help='Número máximo de tentativas de coleta no Provedor OAI-PMH')
    parser.add_argument('-i', '--identifier', help='Código de documento (formato oai:scielo:<PID>)')

    parser.add_argument(
        '-f', 
        '--from_date',
        default='',
        help='Data de processamento até a qual os dados serão considerados para coleta (formato YYYY-MM-DD)',
    )

    parser.add_argument(
        '-u', 
        '--until_date', 
        default=datetime.now().strftime('%Y-%m-%d'), 
        help='Data de processamento a partir da qual os dados serão coletados (formato YYYY-MM-DD)',
    )

    parser.add_argument(
        '-d', 
        '--days_delta', 
        default=3, 
        type=int, 
        help='Número de dias a ser considerado na coleta de dados - é útil quando um dos parâmetros from e until não é informado.',
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
        help='Modo de persistência dos dados coletados',
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Caminho dos dados armazenados: uma string de conexão com banco de dados ou um caminho no disco',
    )

    params = parser.parse_args()

    logging.basicConfig(level=params.logging_level, format='[%(asctime)s] %(levelname)s %(message)s', datefmt='%d/%b/%Y %H:%M:%S')

    oai_client = OAIClient(url=params.oai_address, source_name=SOURCE_NAME, max_retries=params.max_retries, days_delta=params.days_delta)
  
    if params.storage_mode == 'database':
        # instancia client em modo de banco de dados
        raw_client = StorageClientDatabase()
        raw_client.open(params.output)

    elif params.storage_mode == 'json':
        # instancia client em modo de arquivo
        raw_client = StorageClientFile()
        raw_client.open(params.output)

    if params.identifier:
        records = oai_client.get_record(metadata_prefix=params.metadata_prefix, identifier=params.identifier)
    else:
        records = oai_client.get_records(metadata_prefix=params.metadata_prefix, from_date=params.from_date, until_date=params.until_date)

    objects = []

    for r in records:
        objects.append(oai_client.record_to_dict(r))

        if len(objects) == BULK_SIZE:
            raw_client.save(objects)
            objects = []

    if objects:
        raw_client.save(objects)
    raw_client.close()
