from pymongo import MongoClient, uri_parser


def get_mongo_collection(uri):
    puri = uri_parser.parse_uri(uri)
    db = puri.get('database')
    col = puri.get('collection')

    return MongoClient(uri).get_database(db).get_collection(col)
