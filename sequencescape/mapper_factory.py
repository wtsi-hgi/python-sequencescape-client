from abc import ABCMeta, abstractmethod
from sequencescape.model import Model
from sequencescape.database_connector import DatabaseConnector


class MapperFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_mapper(self, model: Model, database_connector: DatabaseConnector):
        """
        TODO
        :param model:
        :param database_connector:
        :return:
        """
        pass