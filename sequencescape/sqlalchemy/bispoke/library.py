from sequencescape.sqlalchemy._sqlalchemy_model import MultiplexedLibrarySQLAlchemyModel
from sequencescape.mapper import Mapper
from sequencescape.common import wrappers


class LibraryMapper(Mapper):

    # TODO: Find out what this means in the domain
    @wrappers.check_args_not_none
    def query_all_multiplexed_libraries_as_batch(self, ids, id_type):
        return self.__get_many_by_given_id(MultiplexedLibrarySQLAlchemyModel, ids, id_type)