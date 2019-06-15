from database import Database
import os
import sys
import argparse
import json

def construct_collection(collection_name, databaseLocation):
    collection_data = {
        "type": "collection",
        "name": collection_name,
        "data": [construct_document(collection_name, i, databaseLocation) for i in os.listdir(os.path.join(databaseLocation, collection_name))]
    }
    return collection_data

def construct_document(collection_name, document_name, databaseLocation):
    document = Database(collection_name, document_name, databaseLocation)
    document_data = {
        "type": "document",
        "name": document_name,
        "data": document.variables
    }
    return document_data

def main(databaseLocation):
    collections = os.listdir(databaseLocation)
    db_data = {
        "type": "database",
        "name": os.path.split(databaseLocation)[-1],
        "data": [construct_collection(i, databaseLocation) for i in collections]
    }
    return db_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dbpath', metavar='path_to_db', type=str, nargs=1,
                    help='Path to your EDMC Local DB')
    args = parser.parse_args()
    print(json.dumps(main(args.dbpath[0])))
