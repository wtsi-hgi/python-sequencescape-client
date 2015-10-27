from sequencescape.sqlalchemy._sqlalchemy_mapper import *
from sequencescape.sqlalchemy._sqlalchemy_database_connector import SQLAlchemyDatabaseConnector


class Connection():
    """
    TODO
    """
    sample = None
    study = None
    well = None
    multiplexed_library = None
    library = None

    def __init__(self, database_uri: str):
        """
        TODO
        :param database_uri:
        :return:
        """
        database_connector = SQLAlchemyDatabaseConnector(database_uri)

        self.sample = SQLAlchemySampleMapper(database_connector)
        self.study = SQLAlchemyStudyMapper(database_connector)
        self.multiplexed_library = SQLAlchemyMultiplexedLibraryMapper(database_connector)
        self.library = SQLAlchemyLibraryMapper(database_connector)
        self.well = SQLAlchemyWellMapper(database_connector)


def connect_to_sequencescape(database_uri: str) -> Connection:
    """
    TODO
    :param database_uri:
    :return:
    """
    return Connection(database_uri)
