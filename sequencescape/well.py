from sequencescape._mapper import *
from sequencescape._sqlalchemy_model import Well


class StudyMapper(Mapper):
    @wrappers.check_args_not_none
    def query_all_wells_as_batch(self, ids, id_type):
        """
        TODO
        :param ids:
        :param id_type:
        :return:
        """
        return self.__get_many(Well, ids, id_type)