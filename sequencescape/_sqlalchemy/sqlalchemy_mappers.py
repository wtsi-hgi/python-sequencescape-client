from typing import Union, List, Any

from sequencescape._sqlalchemy.sqlalchemy_database_connector import SQLAlchemyDatabaseConnector
from sequencescape._sqlalchemy.sqlalchemy_model_converters import convert_to_sqlalchemy_model, convert_to_popo_models,\
    get_equivalent_sqlalchemy_model_type, convert_to_sqlalchemy_models
from sequencescape._sqlalchemy.sqlalchemy_models import SQLAlchemyIsCurrentModel, SQLAlchemySample, SQLAlchemyStudy
from sequencescape.enums import Property
from sequencescape.mappers import Mapper, LibraryMapper, MultiplexedLibraryMapper, SampleMapper, WellMapper, StudyMapper
from sequencescape.models import Model, Library, MultiplexedLibrary, Sample, Well, Study


class SQLAlchemyMapper(Mapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector, model_type: type):
        """
        Default constructor.
        :param database_connector: the object through which database connections can be made
        :param model_type: the type of the model that the mapper is used for
        """
        if not model_type:
            raise ValueError("Model type must be specified through `model_type` parameter")
        if not issubclass(model_type, Model):
            raise ValueError("Model type (%s) must be a subclass of `Model`" % model_type)

        self._database_connector = database_connector
        self._model_type = model_type
        self._sqlalchemy_model_type = get_equivalent_sqlalchemy_model_type(self._model_type)

        if self._sqlalchemy_model_type is None:
            raise NotImplementedError("Not implemented for models of type: `%s`" % model_type)

    def add(self, models: Union[Model, List[Model]]):
        if models is None:
            # TODO: Generalise to anything that's not a subclass of model
            raise ValueError("Cannot add `None`")
        if not isinstance(models, list):
            models = [models]

        session = self._database_connector.create_session()
        for model in models:
            sqlalchemy_model = convert_to_sqlalchemy_model(model)
            session.add(sqlalchemy_model)
        session.commit()
        session.close()

    def get_all(self) -> List[Model]:
        query_model = self._sqlalchemy_model_type
        session = self._database_connector.create_session()
        result = session.query(query_model). \
            filter(query_model.is_current).all()
        session.close()
        assert isinstance(result, list)
        return convert_to_popo_models(result)

    def _get_by_property_value_list(self, property: Property, required_property_values: List[Any]) -> List[Model]:
        # FIXME: Should this always limit `is_current` to 1 - model might not even have this property!
        if not issubclass(self._sqlalchemy_model_type, SQLAlchemyIsCurrentModel):
            raise ValueError(
                "Not possible to get instances of type %s by name as the query required `is_current` property"
                    % self._model_type)

        if len(required_property_values) == 0:
            return []

        query_model = self._sqlalchemy_model_type
        session = self._database_connector.create_session()

        # FIXME: It is an assumption that the Model property has the same name as SQLAlchemyModel
        query_column = query_model.__dict__[property]   # type: Column
        results = session.query(query_model). \
            filter(query_column.in_(required_property_values)). \
            filter(query_model.is_current).all()
        session.close()
        assert isinstance(results, list)
        return convert_to_popo_models(results)


class SQLAlchemySampleMapper(SQLAlchemyMapper, SampleMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        Default constructor.
        :param database_connector: the database connector
        """
        super(SQLAlchemySampleMapper, self).__init__(database_connector, Sample)

    def set_association_with_study(self, samples: Union[Sample, List[Sample]], study: Study):
        if not isinstance(samples, list):
            samples = [samples]

        session = self._database_connector.create_session()

        results = session.query(SQLAlchemySample). \
            filter(SQLAlchemySample.internal_id.in_([sample.internal_id for sample in samples])). \
            all()

        if len(results) == 0:
            raise ValueError("Sample does not exist or does not have an internal_id")

        # FIXME: SQLAlchemy wants to insert the study again when associated to a sample. Could not find out how to stop
        #        this so hacking by deleting from the database. May be a type problem
        session.query(SQLAlchemyStudy).filter(SQLAlchemyStudy.internal_id == study.internal_id).delete()

        sqlalchemy_study = convert_to_sqlalchemy_model(study)
        for result in results:
            result.studies.append(sqlalchemy_study)
        session.commit()
        session.close()

    def get_associated_with_study(self, studies: Union[Study, List[Study]]) -> List[Sample]:
        if not isinstance(studies, list):
            studies = [studies]

        study_internal_ids = [study.internal_id for study in studies]

        session = self._database_connector.create_session()
        results = session.query(SQLAlchemyStudy). \
            filter(SQLAlchemyStudy.internal_id.in_(study_internal_ids)). \
            filter(SQLAlchemyStudy.is_current).all()
        assert isinstance(results, list)

        if len(results) != len(studies):
            raise ValueError("Not all given studies exist in the database.\nGiven: %s\nExisting: %s"
                             % (studies, convert_to_popo_models(results)))

        samples = []
        for result in results:
            for result_sample in result.samples:
                if result_sample not in samples:
                    samples.append(result_sample)
        session.close()

        return convert_to_popo_models(samples)


class SQLAlchemyStudyMapper(SQLAlchemyMapper, StudyMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        Default constructor.
        :param database_connector: the database connector
        """
        super(SQLAlchemyStudyMapper, self).__init__(database_connector, Study)

    def get_associated_with_sample(self, sample_ids: Union[Sample, List[Sample]]) -> List[Study]:
        if not isinstance(sample_ids, list):
            sample_ids = [sample_ids]

        raise NotImplementedError()

        # # FIXME: This implementation is bad - would be better to sort SQLAlchemy models to do the link correctly
        # session = self._database_connector.create_session()
        # studies_samples = session.query(SQLAlchemyStudySamplesLink). \
        #     filter(SQLAlchemyStudySamplesLink.sample_internal_id.in_(sample_ids)). \
        #     filter(SQLAlchemyStudySamplesLink.is_current).all()
        # session.close()
        #
        # if not studies_samples:
        #     return []
        #
        # study_ids = [study_sample.study_internal_id for study_sample in studies_samples]
        # return self.get_by_id(study_ids)


class SQLAlchemyLibraryMapper(SQLAlchemyMapper, LibraryMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        Default constructor.
        :param database_connector: the database connector
        """
        super(SQLAlchemyLibraryMapper, self).__init__(database_connector, Library)


class SQLAlchemyWellMapper(SQLAlchemyMapper, WellMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        Default constructor.
        :param database_connector: the database connector
        """
        super(SQLAlchemyWellMapper, self).__init__(database_connector, Well)


class SQLAlchemyMultiplexedLibraryMapper(SQLAlchemyMapper, MultiplexedLibraryMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        Default constructor.
        :param database_connector: the database connector
        """
        super(SQLAlchemyMultiplexedLibraryMapper, self).__init__(database_connector, MultiplexedLibrary)
