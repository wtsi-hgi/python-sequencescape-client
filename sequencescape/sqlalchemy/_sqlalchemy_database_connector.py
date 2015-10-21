from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sequencescape.database_connector import *


class SQLAlchemyDatabaseConnector(DatabaseConnector):
    _engine = None
    _database_url = None

    def __init__(self, host: str, port: int, database: str, user: str, dialect: str='mysql'):
        """
        TODO
        :param host:
        :param port:
        :param database:
        :param user:
        :param dialect:
        :return:
        """
        self._database_url = '%s://%s:@%s:%s/%s' % (dialect, user, host, port, database)

    def create_session(self):
        """
        TODO
        :return:
        """
        if not self._engine:
            self._engine = create_engine(self._database_url)
        Session = sessionmaker(bind=self._engine)
        session = Session()
        return session
