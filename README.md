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
docker build --tag scieloorg/scielo-nw:0.2.2 .

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
# Using system environment (change the parameters -o, -f, -r, -p and -n as needed)
getter \
  -o https://old.scielo.br/oai/scielo-oai.php \
  -f 2020-04-01 -u 2020-05-01 \
  -r mongodb://user:pass@host:port/scielo_data.raw \
  -p oai_dc_scielo \
  -n oai-old-scl
```

```bash
# Using docker local image (change the parameters -o, -f, -r, -p and -n as needed)
docker run --rm \
  scieloorg/scielo_nw:0.2.2 \
  getter \
  -o https://old.scielo.br/oai/scielo-oai.php \
  -f 2020-04-01 -u 2020-05-01 \
  -r mongodb://user:pass@host:port/scielo_data.raw \
  -p oai_dc_scielo \
  -n oai-old-scl
```

_Command: example 2 - storage mode json_
```bash
# Using system environment, storage mode equals to json, and ommiting default parameters (default protocolo: oai_dc_scielo, default provider: old SciELO Brazil)
getter \
  -f 2020-04-01 \
  -u 2020-05-01 \
  --storage_mode json \
  --output collected_data.jsonl
```

```bash
# Using docker local image (change the parameters -o, -f, -r, -p and -n as needed)
docker run --rm \
  -v /home/user/data:/app/data
  scieloorg/scielo_nw:0.2.2 \
  getter \
  -f 2020-04-01 \
  -u 2020-05-01 \
  --storage_mode json \
  --output /app/data/collected_data.jsonl
```

_Help_
```bash
# getter --help
usage: getter [-h] [-o OAI_ADDRESS] [-n SOURCE_NAME] [-p {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}] [-m MAX_RETRIES] [-i IDENTIFIER] [-f FROM_DATE]
              [-u UNTIL_DATE] [-d DAYS_DELTA] [-l {INFO,WARNING,DEBUG}] [--storage_mode {database,json}] --output OUTPUT

optional arguments:
  -h, --help            show this help message and exit
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
  -f FROM_DATE, --from_date FROM_DATE
                        Data de processamento até a qual os dados serão considerados para coleta (formato YYYY-MM-DD)
  -u UNTIL_DATE, --until_date UNTIL_DATE
                        Data de processamento a partir da qual os dados serão coletados (formato YYYY-MM-DD)
  -d DAYS_DELTA, --days_delta DAYS_DELTA
                        Número de dias a ser considerado na coleta de dados - é útil quando um dos parâmetros from e until não é informado.
  -l {INFO,WARNING,DEBUG}, --logging_level {INFO,WARNING,DEBUG}
                        Modo de logging
  --storage_mode {database,json}
                        Modo de persistência dos dados coletados
  --output OUTPUT       Caminho dos dados armazenados: uma string de conexão com banco de dados ou um caminho no disco
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
SCIELO_NW_OAI_ADDRESS|https://old.scielo.br/oai/scielo-oai.php
SCIELO_NW_SOURCE_NAME|oai-scl
