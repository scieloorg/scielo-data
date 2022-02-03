import logging
import os.path

from util.storage import StorageClient
from pymongo import MongoClient, errors, uri_parser


class StorageClientDatabase(StorageClient):
    def open(self, uri, collection):
        self.client = MongoClient(uri)
        self.db_name, self.col_name = self._extract_db_col_names(uri, collection)

    def _extract_db_col_names(self, uri, collection):
        puri = uri_parser.parse_uri(uri)
        db_name = puri.get('database')
        col_name = puri.get('collection') or collection

        return db_name, col_name

    def save(self, data):
        try:
            self.client.get_database(self.db_name).get_collection(self.col_name).insert_many(data)
        except errors.ServerSelectionTimeoutError as e:
            logging.error(e)

    def close(self):
        self.client.close()


class StorageClientFile(StorageClient):
    def open(self, output_path):
        self._client = self._open_file(output_path)

    def _open_file(self, output_path):
        if os.path.exists(output_path):
            raise FileExistsError(f'{output_path} já existe e não será sobrescrito')

        try:
            return open(output_path, 'w')
        except:
            raise

    def save(self, data):
        for i in data:
            self._client.write(str(i) + '\n')

    def close(self):
        self._client.close()
