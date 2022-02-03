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
docker build --tag scieloorg/scielo-nw:0.2.5 .

# Create a .env.prod to store the required environment variables
```


### Application requirements
1. **Mongo Database** to store the collected data (optional if the storage_mode is `json`)
2. **OAI-PMH Provider** with support to the metadata prefix **OAI DC SciELO**


---
## How to use Getter
Getter is the module responsible for obtaining documents' metadata (incluiding its cited references) from the SciELO OAI-PMH providers.

**Example 1: collecting data from the Old SciELO OAI-PMH Provider and storing the results in a local Mongo database**

_Settings_
- OAI-PMH Provider: Old SciELO Brazil
- Period: 2020-04-01 to 2020-05-01
- Raw database: local Mongo database instance
- Metadata prefix: OAI DC SciELO
- Source name: oai-old-scielo

_Command: example 1 - storage mode database_
```bash
# Using system environment
getter \
  --collection scl \
  --source_name oai-pmh-scl
  --metadata_prefix oai_dc_scielo \
  --storage_mode database \
  --db_connection mongodb://user:pass@host:port/database \
  --oai_address http://old.scielo.br/oai/scielo-oai.php \
  --from_date 2020-04-01 \
  --until_date 2020-05-01
```

```bash
# Using docker image
docker run --rm \
  scieloorg/scielo_nw:0.2.5 \
  getter \
  --collection scl \
  --source_name oai-pmh-scl
  --metadata_prefix oai_dc_scielo \
  --storage_mode database \
  --db_connection mongodb://user:pass@host:port/database \
  --oai_address http://old.scielo.br/oai/scielo-oai.php \
  --from_date 2020-04-01 \
  --until_date 2020-05-01
```

_Command: example 2 - storage mode json_
```bash
# Using system environment
getter \
  --collection scl \
  --source_name oai-pmh-scl \
  --metadata_prefix oai_dc_scielo \
  --storage_mode json \
  --oai_address http://old.scielo.br/oai/scielo-oai.php
  --from_date 2020-04-01 \
  --until_date 2020-04-02
```

```bash
# Using docker image
docker run --rm \
  -v /home/user/data:/app/data
  scieloorg/scielo_nw:0.2.5 \
  getter \
  --collection scl \
  --source_name oai-pmh-scl
  --metadata_prefix oai_dc_scielo \
  --storage_mode json \
  --oai_address http://old.scielo.br/oai/scielo-oai.php \
  --from_date 2020-04-01 \
  --until_date 2020-05-01 \
```

_Help_
```bash
# getter --help
usage: raw_getter.py [-h] -o OAI_ADDRESS -c COLLECTION -n SOURCE_NAME [-p {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}] [-m MAX_RETRIES] [-i IDENTIFIER] [-f FROM_DATE]
                     [-u UNTIL_DATE] [-l {INFO,WARNING,DEBUG}] [--storage_mode {database,json}] [--db_connection DB_CONNECTION] [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -o OAI_ADDRESS, --oai_address OAI_ADDRESS
                        Endereço do site do Provedor OAI-PMH (e.g. https://old.scielo.br/oai/scielo-oai.php)
  -c COLLECTION, --collection COLLECTION
                        Acrônimo da coleção (e.g. scl, ury)
  -n SOURCE_NAME, --source_name SOURCE_NAME
                        Nome da fonte de dados (e.g. oai-old-scl)
  -p {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}, --metadata_prefix {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}
                        Prefixo de metadados
  -m MAX_RETRIES, --max_retries MAX_RETRIES
                        Número máximo de tentativas de coleta no Provedor OAI-PMH
  -i IDENTIFIER, --identifier IDENTIFIER
                        Código de documento (formato oai:scielo:<PID>)
  -f FROM_DATE, --from_date FROM_DATE
                        Data de processamento até a qual os dados serão considerados para coleta (formato YYYY-MM-DD)
  -u UNTIL_DATE, --until_date UNTIL_DATE
                        Data de processamento a partir da qual os dados serão coletados (formato YYYY-MM-DD)
  -l {INFO,WARNING,DEBUG}, --logging_level {INFO,WARNING,DEBUG}
                        Modo de logging
  --storage_mode {database,json}
                        Modo de persistência dos dados coletados
  --db_connection DB_CONNECTION
                        Uma string de conexão com banco de dados
  --output OUTPUT       Um caminho no disco em que os dados serão armazenados
```

## Raw data format

See file [`resources/examples/raw_document.json`](resources/examples/raw_document.json) to verify the structure of the data collected.

---

## Environment variables
Variable | Default value
---------|--------------
SCIELO_NW_BULK_SIZE|10
SCIELO_NW_DB_CONNECTION|mongodb://user:pass@host:port/database.collection
SCIELO_NW_LOGGING_LEVEL|INFO
