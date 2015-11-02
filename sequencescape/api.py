from rfc3987 import match

from sequencescape.sqlalchemy._sqlalchemy_database_connector import SQLAlchemyDatabaseConnector
from sequencescape.sqlalchemy._sqlalchemy_mapper import SQLAlchemySampleMapper, SQLAlchemyMultiplexedLibraryMapper, \
    SQLAlchemyLibraryMapper, SQLAlchemyWellMapper
from sequencescape.sqlalchemy._sqlalchemy_mapper import SQLAlchemyStudyMapper


class Connection():
    """
    Connection manager for queries to the Sequencescape database.
    """
    def __init__(self, database_location: str):
        """
        Default constructor.
        (immutable once set)
        :param database_location: location of the database as an IRI
        """
        if not match(database_location, rule="IRI"):
            raise ValueError("Database location (%s) is not a valid IRI" % database_location)
        self._database_location = database_location

        database_connector = SQLAlchemyDatabaseConnector(database_location)
        self.sample = SQLAlchemySampleMapper(database_connector)
        self.study = SQLAlchemyStudyMapper(database_connector)
        self.multiplexed_library = SQLAlchemyMultiplexedLibraryMapper(database_connector)
        self.library = SQLAlchemyLibraryMapper(database_connector)
        self.well = SQLAlchemyWellMapper(database_connector)


def connect_to_sequencescape(database_uri: str) -> Connection:
    """
    TODO.
    Only opens connections when used...
    :param database_uri:
    :return:
    """
    return Connection(database_uri)