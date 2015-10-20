from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnector():
    """
    Internal database engine used by the ORM.
    """
    _engine = None

    def __init__(self, host, port, database, user, dialect='mysql'):
        """
        TODO
        :param host:
        :param port:
        :param database:
        :param user:
        :param dialect:
        :return:
        """
        database_url = '%s://%s:@%s:%s/%s' % (dialect, user, host, port, database)
        self._engine = create_engine(database_url)

    def create_session(self):
        """
        TODO
        :return:
        """
        if not self._engine:
            raise ConnectionError("Must connect database engine")
        Session = sessionmaker(bind=self._engine)
        session = Session()
        return session

