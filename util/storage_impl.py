import os.path

from util.storage import StorageClient
from pymongo import MongoClient, uri_parser


class StorageClientDatabase(StorageClient):
    def open(self, uri):
        self._client = self._open_mongo(uri)

    def _open_mongo(self, uri):
        puri = uri_parser.parse_uri(uri)
        db = puri.get('database')
        col = puri.get('collection')

        return MongoClient(uri).get_database(db).get_collection(col)

    def save(self, data):
        self._client.insert_many(data)

    def close(self):
        ...


class StorageClientFile(StorageClient):
    def open(self, output_path):
        self._client = self._open_file(output_path)

    def _open_file(self, output_path):
        if os.path.exists(output_path):
            raise FileExistsError

        try:
            return open(output_path, 'w')
        except:
            raise

    def save(self, data):
        for i in data:
            self._client.write(str(i) + '\n')

    def close(self):
        self._client.close()
