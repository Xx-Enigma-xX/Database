import unittest
from database import Database

import random
import string

import os
import shutil

def randomString(length):
    return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(length)])

class LocalDatabaseTest(unittest.TestCase):
    def setUp(self):
        # Setup database
        os.makedirs('./testDatabase')

        # Get random string for user data
        self.user_data = randomString(12)

    def tearDown(self):
        # Clean up
        shutil.rmtree("./testDatabase")

    def test_database_io(self):
        # Saving
        testDatabase = Database('test', 'test', './testDatabase')
        testDatabase.variables['test'] = self.user_data
        testDatabase.save()
        del testDatabase

        # Retrieving
        testDatabase = Database('test', 'test', './testDatabase')
        self.assertEqual(testDatabase.variables['test'], self.user_data)

    def test_saving_and_check_on_filesystem(self):
        # Saving
        testDatabase = Database('test', 'test', './testDatabase')
        testDatabase.variables['test'] = self.user_data
        testDatabase.save()
        del testDatabase

        # Read from Filesystem
        testDatabaseFile = open("./testDatabase/test/test/test", "r")
        testDatabaseFileContent = testDatabaseFile.read()
        testDatabaseFile.close()
        self.assertEqual(testDatabaseFileContent, self.user_data)

if __name__ == '__main__':
    unittest.main()
