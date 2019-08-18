import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os

class Database:
    def __init__(self, databaseName, databaseContainer, databaseLocation=None):
        self.databaseName = databaseName # Collection name
        self.databaseContainer = databaseContainer # Document name
        self.databaseLocation = databaseLocation # Tuple: (Firebase Service Account JSON, Database Name)

        if self.databaseLocation == None:
            self.databaseLocation = os.environ['EDMC_FIRESTORE_DBCRED'].split("//")
        elif type(self.databaseLocation) == type(""):
            self.databaseLocation = (os.environ['EDMC_FIRESTORE_DBCRED'], self.databaseLocation)

        try:
            app = firebase_admin.get_app()
        except ValueError as e:
            cred = credentials.Certificate(self.databaseLocation[0])
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        self.fs_doc = self.db.collection(u"EDMC").document(self.databaseLocation[1]).collection(self.databaseName).document(self.databaseContainer)
        self.variables = self.fs_doc.get().to_dict()

        if self.variables == None:
            self.variables = {}


    def save(self):
        self.fs_doc.set(self.variables)
