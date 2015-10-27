from abc import abstractmethod
from typing import List, Tuple, Union, Any, Optional

from sequencescape.model import *
from sequencescape.enums import Property


#XXX: This interface should use generics (pep-0484). Unfortunately they are not good enough/the documentation is not
#     good enough to use them yet.
class Mapper(metaclass=ABCMeta):
    @abstractmethod
    def add(self, model: Union[Model, List[Model]]):
        """
        TODO
        :param model:
        :return:
        """
        pass

    def get_all(self) -> List[Model]:
        """
        TODO
        :return:
        """
        pass

    @abstractmethod
    def get_by_name(self, names: Union[str, List[str]]) -> Union[Model, List[Model]]:
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
    def get_by_id(self, internal_ids: Union[int, List[int]]) -> Union[Model, List[Model]]:
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
    def get_by_accession_number(self, accession_numbers: Union[str, List[str]]) -> Union[Model, List[Model]]:
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

    def get_by_property_value(
            self,
            property: Union[Property, Union[Tuple[Property, Any]], List[Tuple[Property, Any]]],
            values: Optional[Union[Any, List[Any]]]=None) -> Union[Model, List[Model]]:
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
        if isinstance(property, tuple) or isinstance(property, list):
            return self._get_by_property_value_tuple(property)
        elif isinstance(property, str):
            if isinstance(values, list):
                return self._get_by_property_value_list(property, values)
            else:
                #XXX: If limited to Property enums, would not allow custom properties. If not, why do they exist?
                return self._get_by_property_value_list(property, values)
        else:
            raise ValueError("Invalid arguments")

    @abstractmethod
    def _get_by_property_value_list(
            self, property: Property, values: Union[Any, List[Any]]) -> Union[Model, List[Model]]:
        """
        TODO
        :param property_value_tuples:
        :return:
        """
        pass

    @abstractmethod
    def _get_by_property_value_tuple(
            self, property_value_tuples: Union[Tuple, List[Tuple[Property, Any]]]) -> Union[Model, List[Model]]:
        """
        TODO
        :param property_value_tuples:
        :return:
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
    def get_associated_with_sample(self, sample_internal_ids: str) -> Study:
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