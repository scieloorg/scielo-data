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
