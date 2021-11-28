# SciELO NW
SciELO NW is a repository that contains scripts responsible for obtaining scholarly data from the SciELO Network.


## How to install

### Using system environment
```shell
# Create a virtual environment
virtualenv -p python3.9 .venv

# Access the virtual enviroment
source .venv/bin/activate

# Install dependencies and packages
pip install -r requirements.txt
python setup.py install
```

### Using docker
```shell
# Build the local image
docker build --tag scieloorg/scielo-nw .
```


### Application requirements
1. **Mongo Database** to store the collected data (optional if the storage_mode is `json`)
2. **OAI-PMH Provider** with support to the metadata prefix **OAI DC SciELO**




## How to use

### Getter
Getter is the module responsible for obtaining documents' metadata (incluiding its cited references) from the SciELO OAI-PMH providers.

**Example 1: collecting data from the Old SciELO OAI-PMH Provider and storing it in a local Mongo database**

_Settings_
- OAI-PMH Provider: Old SciELO Brazil
- Period: 2020-04-01 to 2020-05-01
- Raw database: local Mongo database instance
- Metadata prefix: OAI DC SciELO
- Source name: oai-old-scielo

_Command_
```shell
# Using system environment (change the parameters -o, -f, -r, -p and -n as needed)
getter \
-o https://old.scielo.br/oai/scielo-oai.php \
-f 2020-04-01 -u 2020-05-01 \
-r mongodb://user:pass@host:port/scielo_data.raw \
-p oai_dc_scielo \
-n oai-old-scl
```

```shell
# Using docker local image (change the parameters -o, -f, -r, -p and -n as needed)
docker run --rm --name sdr_1 scl-data-raw1:dev getter \
-o https://old.scielo.br/oai/scielo-oai.php \
-f 2020-04-01 -u 2020-05-01 \
-r mongodb://user:pass@host:port/scielo_data.raw \
-p oai_dc_scielo \
-n oai-old-scl

# Using docker official image (change the parameters -o, -f, -r, -p and -n as needed)
docker run --rm --name sdr_1 scieloorg/scielo-data-raw:latest getter \
-o https://old.scielo.br/oai/scielo-oai.php \
-f 2020-04-01 -u 2020-05-01 \
-r mongodb://user:pass@host:port/scielo_data.raw \
-p oai_dc_scielo \
-n oai-old-scl
```

**Help (`getter --help`)**
```
usage: getter [-h] [-f FROM_DATE] [-u UNTIL_DATE] [-d DAYS_DELTA] [-r URI_RAW_DATA] [-o OAI_ADDRESS] [-n SOURCE_NAME] [-p {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}] [-m MAX_RETRIES] [-i IDENTIFIER]

optional arguments:
  -h, --help            show this help message and exit
  -f FROM_DATE, --from_date FROM_DATE
                        Data de processamento até a qual os dados serão considerados para coleta (formato YYYY-MM-DD)
  -u UNTIL_DATE, --until_date UNTIL_DATE
                        Data de processamento a partir da qual os dados serão coletados (formato YYYY-MM-DD)
  -d DAYS_DELTA, --days_delta DAYS_DELTA
                        Número de dias a ser considerado na coleta de dados - é útil quando um dos parâmetros from e until não é informado.
  -r URI_RAW_DATA, --uri_raw_data URI_RAW_DATA
                        String de conexão com banco de dados MongoDB para persistência dos dados coletados (e.g. mongodb://user:pass@localhost:27000/database.raw)
  -o OAI_ADDRESS, --oai_address OAI_ADDRESS
                        Endereço do site do Provedor OAI-PMH (e.g. https://old.scielo.br/oai/scielo-oai.php)
  -n SOURCE_NAME, --source_name SOURCE_NAME
                        Nome da fonte de dados (e.g. oai-old-scl)
  -p {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}, --metadata_prefix {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}
                        Prefixo de metadados
  -m MAX_RETRIES, --max_retries MAX_RETRIES
                        Número máximo de tentativas de coleta no Provedor OAI-PMH
  -i IDENTIFIER, --identifier IDENTIFIER
                        Código de documento (formato oai:scielo:<PID>)
```


**Raw data format**
## Optional environment variables
Setting the following environment variables is optional. You could pass these arguments through command line while calling the getter - see Section Help.

Variable | Default value
---------|--------------
SCIELO_NW_BULK_SIZE|10
SCIELO_NW_OAI_ADDRESS|https://old.scielo.br/oai/scielo-oai.php
SCIELO_NW_SOURCE_NAME|oai-old-scl
