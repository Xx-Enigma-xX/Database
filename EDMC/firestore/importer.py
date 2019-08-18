from .database import Database
import argparse
import json

def main(firestore_credential, data):
    assert data['type'] == "database"
    if firestore_credential[-1] == None or type(firestore_credential) == type(""):
        firestore_credential = (firestore_credential[0], data['name'])
    for collection in data['data']:
        assert collection['type'] == "collection"
        collection_name = collection['name']
        for document in collection['data']:
            assert document['type'] == "document"
            document_name = document['name']
            databaseContainer = Database(collection_name, document_name, firestore_credential)
            databaseContainer.variables = document['data']
            databaseContainer.save()
            del databaseContainer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dbdumppath', metavar='path_to_db_dump', type=str, nargs=1,
                    help='Path to your EDMC DB Dump')
    parser.add_argument('-c', '--cred', metavar='path_to_service_account', type=str, nargs=1,
        help='Path to your GCP service account with permission to access Firestore.')
    parser.add_argument('-n', '--name', metavar='name_of_your_db', type=str, nargs=1,
        help='Name of your EDMC Database on GCP Cloud Firestore')
    args = parser.parse_args()
    with open(args.dbdumppath[0]) as f:
        data = json.load(f)
        f.close()
    main((args.cred[0], args.name[0]), data)
    print("Done!")
