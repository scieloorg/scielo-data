# SciELO Data
SciELO Data is a repository that contains scripts responsible for obtaining, normalizing and merging scholarlry data from the SciELO Network.


## How to install
```shell
# Create a virtual environment
virtualenv -p python3.6 .venv

# Access the virtual enviroment
source .venv/bin/activate

# Install dependencies and binary files
python setup.py install

# Set the database URI connection environment variable__
export URI_RAW_DATA=postgresql://user:pass@host:port/database
```


## How to use

### Getter
Getter is the module responsible for obtaining documents' metadata from the SciELO OAI-PMH providers.

```
usage: getter_raw [-h] -c
                  {arg,bol,nbr,scl,chl,col,cri,cub,ecu,esp,mex,pry,psi,per,prt,pre,ssp,rve,sss,sza,ury,ven,wid,dev}
                  [-d DAYS_DELTA] [-f FROM_DATE] [-m MAX_RETRIES]
                  [-u UNTIL_DATE]
                  [-p {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}]

optional arguments:
  -h, --help            show this help message and exit
  -c {arg,bol,nbr,scl,chl,col,cri,cub,ecu,esp,mex,pry,psi,per,prt,pre,ssp,rve,sss,sza,ury,ven,wid,dev}, --collection {arg,bol,nbr,scl,chl,col,cri,cub,ecu,esp,mex,pry,psi,per,prt,pre,ssp,rve,sss,sza,ury,ven,wid,dev}
  -d DAYS_DELTA, --days_delta DAYS_DELTA
  -f FROM_DATE, --from_date FROM_DATE
  -m MAX_RETRIES, --max_retries MAX_RETRIES
  -u UNTIL_DATE, --until_date UNTIL_DATE
  -p {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}, --metadata_prefix {oai_dc,oai_dc_agris,oai_dc_openaire,oai_dc_scielo}
```

### Normalizer

### Merger
