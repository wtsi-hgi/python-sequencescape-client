from abc import ABCMeta
from typing import TypeVar, Generic, List, Tuple
from sequencescape.common import wrappers
from sequencescape._sqlalchemy_model import SQLAlchemyModel
from sequencescape.enums import IDType
from sequencescape._mapper import Mapper
from sequencescape.database_connector import SQLAlchemyDatabaseConnector


_T = TypeVar('T', bound=SQLAlchemyModel)


class SQLAlchemyMapper(Generic[_T], Mapper[SQLAlchemyDatabaseConnector, _T], metaclass=ABCMeta):
    @wrappers.check_args_not_none
    def get_one(self, name=None, accession_number=None, internal_id=None):
        if name:
            result = self.get_many_by_name(_T, [name])
        elif accession_number:
            result = self.get_many_by_accession_number(_T, [accession_number])
        elif internal_id:
            result = self.get_many_by_internal_id(_T, [internal_id])
        else:
            raise ValueError("No identifier provided to query on.")
        if len(result) > 1:
            raise ValueError("This query has more than one row associated in SEQSCAPE: %s" % [s.name for s in result])
        return result[0]

    @wrappers.check_args_not_none
    def get_many(self, ids_as_tuples):
        results = []
        for id_type, id_val in ids_as_tuples:
            try:
                result_matching_qu = self.get_one(**{'type': _T, id_type: id_val})
            except ValueError:
                print("Multiple entities with the same id found in the DB")
            else:
                if result_matching_qu:
                    results.append(result_matching_qu[0])
        return results

    # XXX: Is this function required?
    @wrappers.check_args_not_none
    def get_many_by_given_id(self, ids, id_type):
        if not ids:
            return []
        if id_type == IDType.NAME:
            return self.get_many_by_name(_T, ids)
        elif id_type == IDType.ACCESSION_NUMBER:
            return self.get_many_by_accession_number(_T, ids)
        elif id_type == IDType.INTERNAL_ID:
            return self.get_many_by_internal_id(_T, ids)
        else:
            raise ValueError("The id_type parameter can only be one of the following: internal_id, accession_number, name.")

    @wrappers.check_args_not_none
    def get_many_by_name(self, names):
        if not names:
            return []
        session = self.get_database_connector().create_session()
        result = session.query(_T). \
            filter(_T.name.in_(names)). \
            filter(_T.is_current == 1).all()
        session.close()
        return result

    @wrappers.check_args_not_none
    def get_many_by_internal_id(self, internal_ids):
        if not internal_ids:
            return []
        session = self.get_database_connector().create_session()
        result = session.query(_T). \
            filter(_T.internal_id.in_(internal_ids)). \
            filter(_T.is_current == 1).all()
        session.close()
        return result

    @wrappers.check_args_not_none
    def get_many_by_accession_number(self, accession_numbers):
        if not accession_numbers:
            return []
        session = self.get_database_connector().create_session()
        result = session.query(_T). \
            filter(_T.accession_number.in_(accession_numbers)). \
            filter(_T.is_current == 1).all()
        session.close()
        return result

    # @wrappers.check_args_not_none
    # def __query_for_study_ids_by_sample_ids(self, sample_internal_ids):
    #     session = self.get_database_connector().create_session()
    #     return session.query(StudySamplesLink). \
    #         filter(StudySamplesLink.sample_internal_id.in_(sample_internal_ids)). \
    #         filter(StudySamplesLink.is_current == 1).all()
