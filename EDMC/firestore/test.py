# This test is yet to be written.

import unittest
from database import Database

import random
import string

import os

def randomString(length):
    return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(length)])

firestore_credential = os.environ['FIRESTORE_CREDENTIAL']

class FirestoreDatabaseTest(unittest.TestCase):
    

if __name__ == '__main__':
    unittest.main()
