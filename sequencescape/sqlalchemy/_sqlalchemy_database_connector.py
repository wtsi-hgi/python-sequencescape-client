from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from sequencescape.sqlalchemy._sqlalchemy_model import *


class SQLAlchemyDatabaseConnector():
    _engine = None
    _database_uri = None

    def __init__(self, uri : str):
        """
        TODO
        :param uri:
        :return:
        """
        self._database_uri = uri

    def create_session(self):
        """
        TODO
        :return:
        """
        if not self._engine:
            self._engine = create_engine(self._database_uri)

        Session = sessionmaker(bind=self._engine)
        session = Session()
        return session
