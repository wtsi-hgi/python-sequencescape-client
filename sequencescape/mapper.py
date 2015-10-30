from abc import abstractmethod, ABCMeta
from typing import List, Tuple, Union, Any, Optional

from sequencescape.model import Model, Study
from sequencescape.enums import Property


# XXX: This interface should use generics (pep-0484). Unfortunately they are not good enough/the documentation is not
#      good enough to use them yet.
class Mapper(metaclass=ABCMeta):
    """
    A data mapper as defined by Martin Fowler (see: http://martinfowler.com/eaaCatalog/dataMapper.html) that moves data
    between objects and a Sequencescape database, while keeping them independent of each other and the mapper itself.
    """
    @abstractmethod
    def add(self, model: Union[Model, List[Model]]):
        """
        Adds data in the given model (of the type this data mapper deals with) to the database.
        :param model: the model containing that data to be transferred
        """
        pass

    def get_all(self) -> List[Model]:
        """
        Gets all the data of the type this data mapper deals with in the Sequencescape database.
        :return: a list of models representing each piece of data in the database of the type this data mapper deals with
        """
        pass

    def get_by_name(self, names: Union[str, List[str]]) -> List[Model]:
        """
        Gets models (of the type this data mapper deals with) of data from the database that have the given name(s).
        :param names: the name or list of names of the data to get models for
        :return: list of models of data with the given name(s)
        """
        results = self.get_by_property_value(Property.NAME, names)
        assert isinstance(results, list)
        return results

    # TODO: This method needs to be tested separately
    def get_by_id(self, internal_ids: Union[int, List[int]]) -> Union[Model, List[Model]]:
        """
        Gets models (of the type this data mapper deals with) of data from the database that have the given id(s).

        The property values this method uses are unique to each entry. Therefore, invoking this method with a single ID
        can return at most one model. For consistency, this return will be a list even if a single ID is used.
        :param internal_ids: the ids or list of ids of the data to get models for
        :return: list of models of data with the given id(s)
        """
        results = self.get_by_property_value(Property.INTERNAL_ID, internal_ids)
        too_many_results_error = "Retrieved multiple entries (%s) with the same internal ID; it has been defined that" \
                                 "this property value should be unqiue. To bypass this check, use:" \
                                 "`get_by_property_value(Property.INTERNAL_ID, internal_ids)`." % results
        if not isinstance(internal_ids, list):
            if len(results) > 1:
                raise ValueError(too_many_results_error)
        else:
            if len(results) > len(internal_ids):
                raise ValueError(too_many_results_error)
        assert isinstance(results, list)
        return results

    def get_by_accession_number(self, accession_numbers: Union[str, List[str]]) -> List[Model]:
        """
        Gets models (of the type this data mapper deals with) of data from the database that have the given accession
        number(s).
        :param accession_numbers: the accession number or list of accession numbers of the data to get models for
        :return: list of models of data with the given accession number(s)
        """
        results = self.get_by_property_value(Property.ACCESSION_NUMBER, accession_numbers)
        assert isinstance(results, list)
        return results

    # TODO: This method needs to be tested separately
    def get_by_property_value(
            self,
            property: Union[Property, Union[Tuple[Property, Any]], List[Tuple[Property, Any]]],
            values: Optional[Union[Any, List[Any]]]=None) -> List[Model]:
        """
        Gets models (of the type this data mapper deals with) of data from the database that have the given property
        values.
        :param property: TODO
        :param values: TODO
        :return: TODO
        """
        if isinstance(property, tuple) or isinstance(property, list):
            results = self._get_by_property_value_tuple(property)
        elif isinstance(property, str):
            if isinstance(values, list):
                results = self._get_by_property_value_list(property, values)
            else:
                # XXX: If limited to Property enums, would not allow custom properties. If not, why do they exist?
                results = self._get_by_property_value_list(property, values)
        else:
            raise ValueError("Invalid arguments")
        assert isinstance(results, list)
        return results

    @abstractmethod
    def _get_by_property_value_list(
            self, property: Property, values: Union[Any, List[Any]]) -> List[Model]:
        """
        Gets models (of the type this data mapper deals with) of data from the database that have one of the given
        values as the value of the given property.
        :param property: the property to match values to
        :param values: the values of the property to match
        :return: models that...
        """
        pass

    @abstractmethod
    def _get_by_property_value_tuple(
            self, property_value_tuples: Union[Tuple, List[Tuple[Property, Any]]]) -> List[Model]:
        """
        TODO
        :param property_value_tuples:
        :return:
        """
        pass


class LibraryMapper(Mapper, metaclass=ABCMeta):
    """
    Mapper for `Library` models.
    """
    pass


class MultiplexedLibraryMapper(Mapper, metaclass=ABCMeta):
    """
    Mapper for `MultiplexedLibrary` models.
    """
    pass


class SampleMapper(Mapper, metaclass=ABCMeta):
    """
    Mapper for `Sample` models.
    """
    pass


class WellMapper(Mapper, metaclass=ABCMeta):
    """
    Mapper for `Well` models.
    """
    pass


class StudyMapper(Mapper, metaclass=ABCMeta):
    """
    Mapper for `Study` models.
    """
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