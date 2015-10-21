from sequencescape.database_connector import *


class DummyDatabaseConnector(DatabaseConnector):
    def create_session(self):
        print("Dummy database connnector doesn't do anything")

