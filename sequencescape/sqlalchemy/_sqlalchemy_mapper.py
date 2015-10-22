from sequencescape.sqlalchemy._sqlalchemy_model_converter import *
from sequencescape.sqlalchemy._sqlalchemy_database_connector import *
from sequencescape.sqlalchemy._sqlalchemy_model import *
from sequencescape.mapper import *


class _SQLAlchemyMapper(Mapper):
    _database_connector = None
    _type_cache = None
    _model_type = None

    def __init__(self, database_connector: SQLAlchemyDatabaseConnector, model_type: type) -> None:
        """
        Default constructor.
        :param database_connector: the object through which database connections can be made
        :param model_type: the type of the model that the mapper is used for
        """
        if not model_type:
            raise ValueError("Model type must be specified through `model_type` parameter")
        if not issubclass(model_type, Model):
            raise ValueError("Model type must be a subclass of Model")
        self._model_type = model_type

    def get_one(self, name=None, accession_number=None, internal_id=None):
        if name:
            result = self.get_many_by_name([name])
        elif accession_number:
            result = self.get_many_by_accession_number([accession_number])
        elif internal_id:
            result = self.get_many_by_internal_id([internal_id])
        else:
            raise ValueError("No identifier provided to query on.")
        if len(result) > 1:
            raise ValueError("This query has more than one row associated in SEQSCAPE: %s" % [s.name for s in result])
        return result[0]

    def get_many(self, ids_as_tuples):
        results = []
        for id_type, id_val in ids_as_tuples:
            try:
                result_matching_qu = self.get_one(**{'type': self._get_sqlalchemy_model_type(), id_type: id_val})
            except ValueError:
                print("Multiple entities with the same id found in the DB")
            else:
                if result_matching_qu:
                    results.append(result_matching_qu)
        return results

    def get_many_by_given_id(self, ids, id_type):
        if not ids:
            return []
        if id_type == IDType.NAME:
            return self.get_many_by_name(ids)
        elif id_type == IDType.ACCESSION_NUMBER:
            return self.get_many_by_accession_number(ids)
        elif id_type == IDType.INTERNAL_ID:
            return self.get_many_by_internal_id(ids)
        else:
            raise ValueError("The id_type parameter must be a value linked to by an IDType enum.")

    def get_many_by_name(self, names):
        if not names:
            return []

        session = self.__get_database_connector().create_session()
        # XXX: Given generics aren't possible, should hint type with # type: XXX comment. However, it is unclear how
        #      to hint multiple interfaces!
        model_type = self._get_sqlalchemy_model_type()
        if not issubclass(model_type, SQLAlchemyNamed):
            raise ValueError(
                "Not possible to get instances of type %s by name as they do not have that property" % self.__get_model_type())
        if not issubclass(model_type, SQLAlchemyIsCurrent):
            raise ValueError(
                "Not possible to get instances of type %s by name as the query required `is_current` property"
                    % self.__get_model_type())

        result = session.query(model_type). \
            filter(model_type.name.in_(names)). \
            filter(model_type.is_current == 1).all()
        session.close()

        return convert_to_popo_model(result)

    def get_many_by_internal_id(self, internal_ids):
        if not internal_ids:
            return []

        session = self.__get_database_connector().create_session()
        model_type = self._get_sqlalchemy_model_type()
        if not issubclass(model_type, SQLAlchemyNamed):
            raise ValueError(
                "Not possible to get instances of type %s by internal ID as they do not have that property" % self.__get_model_type())
        if not issubclass(model_type, SQLAlchemyIsCurrent):
            raise ValueError(
                "Not possible to get instances of type %s by internal ID as the query requires `is_current` property" % self.__get_model_type())

        result = session.query(model_type). \
            filter(model_type.internal_id.in_(internal_ids)). \
            filter(model_type.is_current == 1).all()
        session.close()

        return convert_to_popo_model(result)

    def get_many_by_accession_number(self, accession_numbers):
        if not accession_numbers:
            return []

        session = self.__get_database_connector().create_session()
        model_type = self._get_sqlalchemy_model_type()
        if not issubclass(model_type, SQLAlchemyNamed):
            raise ValueError(
                "Not possible to get instances of type %s by accession number as they do not have that property" % self.__get_model_type())
        if not issubclass(model_type, SQLAlchemyIsCurrent):
            raise ValueError(
                "Not possible to get instances of type %s by accession number as the query requires `is_current` property" % self.__get_model_type())

        result = session.query(model_type). \
            filter(model_type.accession_number.in_(accession_numbers)). \
            filter(model_type.is_current == 1).all()
        session.close()

        return convert_to_popo_model(result)

    def __get_database_connector(self):
        """
        Gets the object through which database connections can be made.
        :return: the database connector
        """
        assert self._database_connector
        return self._database_connector

    def _get_sqlalchemy_model_type(self):
        """
        TODO
        :return:
        """
        if not self._type_cache:
            self._type_cache = get_equivalent_sqlalchemy_model_type(self.__get_model_type())
            assert issubclass(self._type_cache, SQLAlchemyModel)
        return self._type_cache

    def __get_model_type(self) -> type:
        """
        Gets the type of models that this mapper deals with
        :return: the type of models that this mapper deals with
        """
        assert self._model_type
        return self._model_type


class SQLAlchemyLibraryMapper(_SQLAlchemyMapper, LibraryMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemyLibraryMapper, self).__init__(database_connector, SQLAlchemyStudy)


class SQLAlchemyMultiplexedLibraryMapper(_SQLAlchemyMapper, MultiplexedLibraryMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemyMultiplexedLibraryMapper, self).__init__(database_connector, SQLAlchemyMultiplexedLibrary)


class SQLAlchemySampleMapper(_SQLAlchemyMapper, SampleMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemySampleMapper, self).__init__(database_connector, SQLAlchemySample)


class SQLAlchemyWellMapper(_SQLAlchemyMapper, WellMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemyWellMapper, self).__init__(database_connector, SQLAlchemyWell)


class SQLAlchemyStudyMapper(_SQLAlchemyMapper, StudyMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemyStudyMapper, self).__init__(database_connector, SQLAlchemyStudy)

    def get_many_associated_with_samples(self, sample_internal_ids: str) -> Study:
        session = self.__get_database_connector().create_session()

        studies_samples = session.query(SQLAlchemyStudySamplesLink). \
            filter(SQLAlchemyStudySamplesLink.sample_internal_id.in_(sample_internal_ids)). \
            filter(SQLAlchemyStudySamplesLink.is_current == 1).all()

        if not studies_samples:
            return []

        study_ids = [study_sample.study_internal_id for study_sample in studies_samples]
        return self.get_many_by_internal_id(study_ids)
