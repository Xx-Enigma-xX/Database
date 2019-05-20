import os
import shutil

class Database:
    def __init__(self, databaseName, databaseContainer, databaseLocation="./database"):
        self.databaseName = databaseName
        self.databaseContainer = databaseContainer
        self.databaseLocation = databaseLocation
        self.variables = {}
        try:
            os.mkdir("%s/%s" % (self.databaseLocation, self.databaseName))
        except:
            pass
        try:
            os.mkdir("%s/%s/%s" % (self.databaseLocation, self.databaseName, self.databaseContainer))
        except:
            pass
        for i in os.listdir("%s/%s/%s" % (self.databaseLocation, self.databaseName, self.databaseContainer)):
            fileObject = open("%s/%s/%s/%s" % (self.databaseLocation, self.databaseName, self.databaseContainer, i), "r")
            self.variables[i] = fileObject.read()
            # eval("self.%s = '%s'" % (i, fileObject.read()))
            fileObject.close()

    def save(self):
        shutil.rmtree("%s/%s/%s" % (self.databaseLocation, self.databaseName, self.databaseContainer))
        os.mkdir("%s/%s/%s" % (self.databaseLocation, self.databaseName, self.databaseContainer))
        for i in list(self.variables.keys()):
            fileObject = open("%s/%s/%s/%s" % (self.databaseLocation, self.databaseName, self.databaseContainer, i), "w")
            fileObject.write(self.variables[i])
            fileObject.close()
