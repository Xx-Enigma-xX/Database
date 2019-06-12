# import unittest
# from database import Database
#
# import random
# import string
#
# import sys
# from pymongo import MongoClient
#
# def randomString(length):
#     return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(length)])
#
# class LocalDatabaseTest(unittest.TestCase):
#     def setUp(self):
#         # Get credentials
#         self.database_endpoint = sys.environ['EDMC_MONGO_ENDPOINT']
#         self.database_endpointport = sys.environ['EDMC_MONGO_ENDPOINTPORT']
#         self.database_name = sys.environ['EDMC_MONGO_DATABASENAME']
#         self.database_username = sys.environ['EDMC_MONGO_USERNAME']
#         self.database_password = sys.environ['EDMC_MONGO_PASSWORD']
#         self.database_authsource = sys.environ['EDMC_MONGO_AUTHSOURCE']
#         self.database_authmechanism = sys.environ['EDMC_MONGO_AUTOMECHANISM']
#         self.mongo_uri = "{0}:{1}:{2}".format(self.database_endpoint, self.database_endpointport, self.database_name)
#
#         # Get random string for user data
#         self.user_data = randomString(12)
#
#     def tearDown(self):
#         # Clean up
#         client = MongoClient(self.mongo_uri)
#         client.drop_database('test_database')
#
#     def test_database_io(self):
#         # Saving
#         testDatabase = Database('test', 'test', self.mongo_uri)
#         testDatabase.variables['test'] = self.user_data
#         testDatabase.save()
#         del testDatabase
#
#         # Retrieving
#         testDatabase = Database('test', 'test', self.mongo_uri)
#         self.assertEqual(testDatabase.variables['test'], self.user_data)
#
#     def test_saving_and_check_on_mongo(self):
#         # Saving
#         testDatabase = Database('test', 'test', self.mongo_uri)
#         testDatabase.variables['test'] = self.user_data
#         testDatabase.save()
#         del testDatabase
#
#         # Read from MongoDB
#         client = MongoClient(self.mongo_uri)
#         testDatabaseDocumentContent = client.test_database.test.find_one({"_doc_title": "test"})['test']
#         self.assertEqual(testDatabaseDocumentContent, self.user_data)
#
# if __name__ == '__main__':
#     unittest.main()

"""
Test not yet implemented
"""
