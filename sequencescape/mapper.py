from abc import abstractmethod
from typing import List, Tuple
from sequencescape.model import *
from sequencescape.enums import IDType


#XXX: This interface should use generics (pep-0484). Unfortunately they are not good enough/the documentation is not
#     good enough to use them yet.
class Mapper(metaclass=ABCMeta):
    @abstractmethod
    def get(self, name: str=None, accession_number: str=None, internal_id: str=None) :
        """
        This function queries on the entity of type type, by one (and only one) of the identifiers:
        name, accession_number, internal_id and returns the results found in Seqscape corresponding to
        that identifier. Since it is expecting one result per identifier, it throws a ValueError if there
        are multiple rows in the DB corresponding to that identifier.
        Note: only one identifier should be provided
        Parameters
        ----------
        type : class
        The type of model to be queried on and returned. Can be: models.Sample or models.Study or models.Library
        name : str
        The name of the entity to query on
        accession_number : str
        The accession number of the entity to query on
        Returns
        -------
        result : type type
        The entity found in the database to have the identifier given as parameter
        Raises
        ------
        ValueError - if there are more rows corresponding to the identifier provided as param
        """
        pass

    @abstractmethod
    def get_many(self, ids_as_tuples: List[Tuple[IDType, str]]):
        """
        TODO
        :param model_type:
        :param ids_as_tuples:
        :return:
        """
        pass

    @abstractmethod
    def get_many_by_given_id(self, ids: List[str], id_type: IDType):
        """
        This function is for internal use - it queries seqscape for all the entities or type type
        and returns a list of results.
        Parameters
        ----------
        name_list
        The list of names for the entities you want to query about
        accession_number_list
        The list of accession numbers for all the entities you want to query about
        internal_id_list
        The list of internal_ids for all the entities you want to query about
        Returns
        -------
        obj_list
        A list of objects returned by the query of type models.*
        """
        pass

    @abstractmethod
    def get_many_by_name(self, names: List[str]):
        """
        This function queries the database for all the entity names given as parameter as a batch.
        Parameters
        ----------
        engine
        Database engine to run the queries on
        type
        A model class - predefined in serapis.seqscape.models e.g. Sample, Study
        keys
        A list of keys (name) to run the query for
        Returns
        -------
        obj_list
        Returns a list of objects of type type found to match the keys given as parameter.
        """
        pass

    @abstractmethod
    def get_many_by_internal_id(self, internal_ids: List[str]):
        """
        This function queries the database for all the entity internal ids given as parameter as a batch.
        Parameters
        ----------
        engine
        Database engine to run the queries on
        type
        A model class - predefined in serapis.seqscape.models e.g. Sample, Study
        keys
        A list of internal_ids to run the query for
        Returns
        -------
        obj_list
        Returns a list of objects of type type found to match the internal_ids given as parameter.
        """
        pass

    @abstractmethod
    def get_many_by_accession_number(self, accession_numbers: List[str]):
        """
        This function queries the database for all the entity accession_number given as parameter as a batch.
        Parameters
        ----------
        engine
        Database engine to run the queries on
        type
        A model class - predefined in serapis.seqscape.models e.g. Sample, Study
        keys
        A list of accession_number to run the query for
        Returns
        -------
        obj_list
        Returns a list of objects of type type found to match the accession_number given as parameter.
        """
        pass


class LibraryMapper(Mapper, metaclass=ABCMeta):
    pass


class MultiplexedLibraryMapper(Mapper, metaclass=ABCMeta):
    pass


class SampleMapper(Mapper, metaclass=ABCMeta):
    pass


class WellMapper(Mapper, metaclass=ABCMeta):
    pass


class StudyMapper(Mapper, metaclass=ABCMeta):
    @abstractmethod
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
        pass