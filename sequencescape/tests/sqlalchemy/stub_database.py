import tempfile

from sqlalchemy import create_engine

from sequencescape._sqlalchemy.sqlalchemy_models import SQLAlchemyModel


def create_stub_database():
    """
    Creates a stub database with a number of tables found in a Sequencescape database.

    An in-memory database is not used because sqlite in-memory databases are destroyed upon close.
    :return: stub database
    """
    file_handle, database_location = tempfile.mkstemp()
    dialect = "sqlite"

    engine = create_engine("sqlite:///%s" % database_location)
    SQLAlchemyModel.metadata.create_all(bind=engine)

    return database_location, dialect
