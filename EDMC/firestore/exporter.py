from .database import Database
import os
import sys
import argparse
import json
import os
import subprocess

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def get_subcollections(cred, path):
    module_path = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(['node', module_path + '/get_subcollections.js', cred, path], capture_output=True)
    result = result.stdout.decode("utf-8")[:-1].split(",")
    if result == ['']:
        return []
    else:
        return result

def construct_collection(collection_name, databaseLocation, db):
    docs = db.collection(u'EDMC').document(databaseLocation).collection(collection_name).stream()
    collection_data = {
        "type": "collection",
        "name": collection_name,
        "data": [construct_document(collection_name, i.id, databaseLocation, db) for i in docs]
    }
    return collection_data

def construct_document(collection_name, document_name, databaseLocation, db):
    document = Database(collection_name, document_name, databaseLocation)
    document_data = {
        "type": "document",
        "name": document_name,
        "data": document.variables
    }
    return document_data

def main(databaseInfo):
    db = get_fb_cred(databaseInfo[0])
    db_name = databaseInfo[1]
    collections = db.collection(u'EDMC').document(db_name)
    db_data = {
        "type": "database",
        "name": db_name,
        "data": [construct_collection(i, db_name, db) for i in get_subcollections(databaseInfo[0], 'EDMC/{0}'.format(db_name))]
    }
    return db_data

def get_fb_cred(cert_location):
    try:
        app = firebase_admin.get_app()
    except ValueError as e:
        cred = credentials.Certificate(cert_location)
        firebase_admin.initialize_app(cred)
    return firestore.client()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fbcred', metavar='firebase_credentials', type=str, nargs=1,
                    help='Credentials to access Firebase Cloud Firestore')
    parser.add_argument('db_name', metavar='database_name', type=str, nargs=1,
                    help='Name of the Database on Firebase Cloud Firestore')
    args = parser.parse_args()
    print(json.dumps(main((args.fbcred[0], args.db_name[0]))))
