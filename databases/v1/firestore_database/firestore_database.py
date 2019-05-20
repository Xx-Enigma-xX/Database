import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Database:
    def __init__(self, databaseName, databaseContainer, databaseLocation):
        self.databaseName = databaseName # Collection name
        self.databaseContainer = databaseContainer # Document name
        self.databaseLocation = databaseLocation # Credentials (Firebase Service Account JSON)

        cred = credentials.Certificate(credentials)
        firebase_admin.initialize_app(self.databaseLocation)
        self.db = firestore.client()

        self.fs_doc = db.collection(self.databaseName).document(self.databaseContainer)
        self.variables = self.fs_doc.get().to_dict()


    def save(self):
        self.fs_doc.set(self.variables)
