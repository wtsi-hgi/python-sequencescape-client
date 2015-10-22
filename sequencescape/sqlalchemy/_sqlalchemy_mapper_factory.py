from sequencescape.mapper_factory import *


class SQLAlchemyMapperFactory(MapperFactory):
    def create_mapper(self, model: Model, database_connector: DatabaseConnector):
        pass