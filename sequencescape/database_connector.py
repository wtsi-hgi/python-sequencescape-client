from abc import ABCMeta, abstractmethod


class DatabaseConnector(metaclass=ABCMeta):
    @abstractmethod
    def create_session(self):
        """
        Creates a database connection and returns the session.
        :return: the database connection session
        """
        pass