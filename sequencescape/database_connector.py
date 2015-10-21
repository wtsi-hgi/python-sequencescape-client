from abc import ABCMeta, abstractmethod


class DatabaseConnector(metaclass=ABCMeta):
    @abstractmethod
    def create_session(self):
        """
        """
        pass