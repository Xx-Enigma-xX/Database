# This test is yet to be written.

import unittest
from database import Database

import uuid

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firestore_credential = os.environ['FIRESTORE_CREDENTIAL']

class FirestoreDatabaseTest(unittest.TestCase):
    def setUp(self):
        # Setup credentials
        # Use a service account
        try:
            app = firebase_admin.get_app()
        except ValueError as e:
            cred = credentials.Certificate(firestore_credential)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        # Get random string for user data
        self.test_data = uuid.uuid4().hex
        self.test_data2 = uuid.uuid4().hex
        self.assertNotEqual(self.test_data, self.test_data2, msg="An error occured while generating test data. Please retry. Also celebrate the fact that your computer generated two equal UUIDs.")

    def tearDown(self):
        # Clean up
        self.db.collection(u'EDMC').document(u'_test').collection(u'_test').document(u'_test').delete()
        self.db.collection(u'EDMC').document(u'_test').delete()

    def test_database_io(self):
        # Saving through Firebase API
        doc_ref = self.db.collection(u'EDMC').document(u'_test').collection(u'_test').document(u'_test')
        doc_ref.set({
            u'test': self.test_data,
        })
        del doc_ref

        # Retrieving through EDMC Firestore v1
        testDatabase = Database('_test', '_test', firestore_credential)
        self.assertEqual(testDatabase.variables['test'], self.test_data)
        del testDatabase

        # Modifying through EDMC Firestore v1
        testDatabase = Database('_test', '_test', firestore_credential)
        testDatabase.variables['test'] = self.test_data2
        testDatabase.save()
        del testDatabase

        # Retreving through Firebase API
        doc_ref = db.collection(u'EDMC').document(u'_test').collection(u'_test').document(u'_test')
        doc = doc_ref.get()
        self.assertEqual(self.test_data2, doc.to_dict()['test'])

if __name__ == '__main__':
    unittest.main()
