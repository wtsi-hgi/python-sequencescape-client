from sequencescape.sqlalchemy._sqlalchemy_mapper import *
from sequencescape.sqlalchemy._sqlalchemy_database_connector import SQLAlchemyDatabaseConnector

def connect_to_sequencescape(database_uri: str):
    return Connection(database_uri)


class Connection():
    def __init__(self, database_uri: str):
        database_connector = SQLAlchemyDatabaseConnector(database_uri)

        self.sample = SQLAlchemySampleMapper(database_connector)
        self.study = SQLAlchemySampleMapper(database_connector)
        self.well = SQLAlchemySampleMapper(database_connector)
        self.multiplexed_library = SQLAlchemySampleMapper(database_connector)
        self.library = SQLAlchemySampleMapper(database_connector)
        self.well = SQLAlchemySampleMapper(database_connector)

