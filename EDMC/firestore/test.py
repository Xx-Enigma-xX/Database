import unittest
from .database import Database
from .exporter import main as export_db
from .importer import main as import_db

import uuid
import logging

import os
import subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firestore_credential = os.environ['EDMC_FIRESTORE_DBCRED']

def get_firestore_credentials(firestore_credential=firestore_credential):
    # Use a service account
    try:
        app = firebase_admin.get_app()
    except ValueError as e:
        cred = credentials.Certificate(firestore_credential)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def teardown_tests(db):
    db.collection(u'EDMC').document(u'_test').collection(u'_test').document(u'_test').delete()
    db.collection(u'EDMC').document(u'_test').delete()

class FirestoreDatabaseIOTest(unittest.TestCase):
    def setUp(self):
        # Setup credentials
        self.db = get_firestore_credentials()

        # Get random string for user data
        self.test_data = uuid.uuid4().hex
        self.test_data2 = uuid.uuid4().hex
        self.assertNotEqual(self.test_data, self.test_data2, msg="An error occured while generating test data. Please retry. Also celebrate the fact that your computer generated two equal UUIDs.")

    def tearDown(self):
        # Clean up
        teardown_tests(self.db)

    def test_database_io(self):
        # Saving through Firebase API
        doc_ref = self.db.collection(u'EDMC').document(u'_test').collection(u'_test').document(u'_test')
        doc_ref.set({
            u'test': self.test_data,
        })
        del doc_ref

        # Retrieving through EDMC Firestore v1
        testDatabase = Database('_test', '_test', (firestore_credential, "_test"))
        self.assertEqual(testDatabase.variables['test'], self.test_data)
        del testDatabase

        # Modifying through EDMC Firestore v1
        testDatabase = Database('_test', '_test', (firestore_credential, "_test"))
        testDatabase.variables['test'] = self.test_data2
        testDatabase.save()
        del testDatabase

        # Retreving through Firebase API
        doc_ref = self.db.collection(u'EDMC').document(u'_test').collection(u'_test').document(u'_test')
        doc = doc_ref.get()
        self.assertEqual(self.test_data2, doc.to_dict()['test'])

class FirestoreDatabaseExportTest(unittest.TestCase):
    def setUp(self):
        # Setup credentials
        self.db = get_firestore_credentials()

        # Get random string for user data
        self.test_data = uuid.uuid4().hex

    def tearDown(self):
        # Clean up
        teardown_tests(self.db)

    def test_save_through_EDMC_and_read_with_exporter(self):
        # Save through Firestore EDMC interface
        testDatabase = Database('_test', '_test', (firestore_credential, "_test"))
        testDatabase.variables['test'] = self.test_data
        testDatabase.save()
        del testDatabase

        # Read through Firestore EDMC Exporter
        exported_data = export_db((firestore_credential, "_test"))
        expected_exported_data = {
            "type": "database",
            "name": "_test",
            "data": [
                {
                    "type": "collection",
                    "name": "_test",
                    "data": [
                        {
                            "type": "document",
                            "name": "_test",
                            "data": {
                                "test": self.test_data
                            }
                        }
                    ]
                }
            ]
        }
        self.assertEqual(exported_data, expected_exported_data)


class FirestoreDatabaseImportTest(unittest.TestCase):
    def setUp(self):
        # Setup credentials
        self.db = get_firestore_credentials()

        # Get random string for user data
        self.test_data = uuid.uuid4().hex

    def tearDown(self):
        # Clean up
        teardown_tests(self.db)

    def test_save_through_importer_and_read_with_EDMC(self):
        # Save through EDMC Firestore Importer
        data_to_import = {
            "type": "database",
            "name": "_test",
            "data": [
                {
                    "type": "collection",
                    "name": "_test",
                    "data": [
                        {
                            "type": "document",
                            "name": "_test",
                            "data": {
                                "test": self.test_data
                            }
                        }
                    ]
                }
            ]
        }
        import_db(firestore_credential, data_to_import)

        # Read through EDMC Firestore
        testDatabase = Database('_test', '_test', (firestore_credential, "_test"))
        self.assertEqual(self.test_data, testDatabase.variables['test'])


class FirestoreDatabaseSubcollectionRetreiverTest(unittest.TestCase):
    def setUp(self):
        # Setup credentials
        self.db = get_firestore_credentials()

        # Setup subcollections
        self.db.collection(u'EDMC').document(u'_test').collection(u'_test1').document(u'_test').collection(u'_test3').document(u'_test').set({})
        self.db.collection(u'EDMC').document(u'_test').collection(u'_test1').document(u'_test').collection(u'_test4').document(u'_test').set({})
        self.db.collection(u'EDMC').document(u'_test').collection(u'_test2').document(u'_test').set({})

    def tearDown(self):
        # Clean up
        self.db.collection(u'EDMC').document(u'_test').collection(u'_test1').document(u'_test').collection(u'_test3').document(u'_test').delete()
        self.db.collection(u'EDMC').document(u'_test').collection(u'_test1').document(u'_test').collection(u'_test4').document(u'_test').delete()
        self.db.collection(u'EDMC').document(u'_test').collection(u'_test2').document(u'_test').delete()

    def test_retreiving_list_of_subcollections_two_levels_deep(self):
        result = subprocess.run(['node', 'EDMC/firestore/get_subcollections.js', firestore_credential, 'EDMC/_test'], capture_output=True)
        subcollections = result.stdout.decode("utf-8")[:-1].split(",")
        self.assertEqual(subcollections, ['_test1', '_test2'])

    def test_retreiving_list_of_subcollections_four_levels_deep(self):
        result = subprocess.run(['node', 'EDMC/firestore/get_subcollections.js', firestore_credential, 'EDMC/_test/_test1/_test'], capture_output=True)
        subcollections = result.stdout.decode("utf-8")[:-1].split(",")
        self.assertEqual(subcollections, ['_test3', '_test4'])

if __name__ == '__main__':
    unittest.main()
