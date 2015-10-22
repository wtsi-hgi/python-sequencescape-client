from sequencescape.sqlalchemy._sqlalchemy_mapper import SQLAlchemyMapper
from sequencescape.sqlalchemy._sqlalchemy_database_connector import *
from sequencescape.sqlalchemy._sqlalchemy_model import *
from sequencescape.model import *


class SQLAlchemyLibraryMapper(SQLAlchemyMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemyLibraryMapper, self).__init__(database_connector, SQLAlchemyStudy)


class SQLAlchemyMultiplexedLibraryMapper(SQLAlchemyMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemyMultiplexedLibraryMapper, self).__init__(database_connector, SQLAlchemyMultiplexedLibrary)


class SQLAlchemySampleMapper(SQLAlchemyMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemySampleMapper, self).__init__(database_connector, SQLAlchemySample)


class SQLAlchemyWellMapper(SQLAlchemyMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemyWellMapper, self).__init__(database_connector, SQLAlchemyWell)


class SQLAlchemyStudyMapper(SQLAlchemyMapper):
    def __init__(self, database_connector: SQLAlchemyDatabaseConnector):
        """
        TODO
        :param database_connector:
        :return:
        """
        super(SQLAlchemyStudyMapper, self).__init__(database_connector, SQLAlchemyStudy)

    def get_many_associated_with_samples(self, sample_internal_ids: str) -> Study:
        """
        This function fetches from seqeuencescape all the studies that the samples given as parameter belong to.
        Parameters
        ----------
        sample_internal_ids : list
            A list of sample internal_id values, for which you wish to find out the study/studies
        Returns
        -------
        studies : list
            A list of models.Study found for the samples given as parameter by sample_internal_ids
        """
        session = self.__get_database_connector().create_session()

        studies_samples = session.query(SQLAlchemyStudySamplesLink). \
            filter(SQLAlchemyStudySamplesLink.sample_internal_id.in_(sample_internal_ids)). \
            filter(SQLAlchemyStudySamplesLink.is_current == 1).all()

        if not studies_samples:
            return []

        study_ids = [study_sample.study_internal_id for study_sample in studies_samples]
        return self.get_many_by_internal_id(study_ids)
