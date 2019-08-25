from .database import Database
import argparse
import json

def main(databaseLocation, data):
    assert data['type'] == "database"
    for collection in data['data']:
        assert collection['type'] == "collection"
        collection_name = collection['name']
        for document in collection['data']:
            assert document['type'] == "document"
            document_name = document['name']
            databaseContainer = Database(collection_name, document_name, databaseLocation)
            databaseContainer.variables = document['data']
            databaseContainer.save()
            del databaseContainer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dbdumppath', metavar='path_to_db_dump', type=str, nargs=1,
                    help='Path to your EDMC DB Dump')
    parser.add_argument('-c', '--cred', metavar='path_to_db', type=str, nargs=1,
        help='Path to your EDMC Local DB.')
    args = parser.parse_args()
    with open(args.dbdumppath[0]) as f:
        data = json.load(f)
        f.close()
    main(args.cred[0], data)
    print("Done!")
