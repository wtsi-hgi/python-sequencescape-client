from abc import abstractmethod, ABCMeta
from typing import List, Tuple, Union, Any, Optional

from sequencescape.model import Model, Study, NamedModel, InternalIdModel, AccessionNumberModel
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

    # TODO: This method needs to be tested independently of concrete subclass.
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
        :return: models that have at least one property value defined in the given list of acceptable values
        """
        pass

    @abstractmethod
    def _get_by_property_value_tuple(
            self, property_value_tuples: Union[Tuple, List[Tuple[Property, Any]]]) -> List[Model]:
        """
        Gets models (of the type this data mapper deals with) of data from the database that have have one of the
        property values defined in a tuple from the given list.
        :param property_value_tuples: the tuples declaring what property values to match
        :return: models that have at least one property value defined in the given tuple list
        """
        pass


class NamedMapper(Mapper, metaclass=ABCMeta):
    """
    TODO
    """
    # TODO: This method needs to be tested independently of concrete subclass.
    def get_by_name(self, names: Union[str, List[str]]) -> List[NamedModel]:
        """
        Gets models (of the type this data mapper deals with) of data from the database that have the given name(s).
        :param names: the name or list of names of the data to get models for
        :return: list of models of data with the given name(s)
        """
        results = self.get_by_property_value(Property.NAME, names)
        assert isinstance(results, list)
        return results


class InternalIDMapper(Mapper, metaclass=ABCMeta):
    """
    TODO
    """
    # TODO: This method needs to be tested independently of concrete subclass.
    def get_by_id(self, internal_ids: Union[int, List[int]]) -> Union[Model, List[InternalIdModel]]:
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


class AccessionNumberMapper(Mapper, metaclass=ABCMeta):
    # TODO: This method needs to be tested independently of concrete subclass.
    def get_by_accession_number(self, accession_numbers: Union[str, List[str]]) -> List[AccessionNumberModel]:
        """
        Gets models (of the type this data mapper deals with) of data from the database that have the given accession
        number(s).
        :param accession_numbers: the accession number or list of accession numbers of the data to get models for
        :return: list of models of data with the given accession number(s)
        """
        results = self.get_by_property_value(Property.ACCESSION_NUMBER, accession_numbers)
        assert isinstance(results, list)
        return results


class SampleMapper(NamedMapper, InternalIDMapper, AccessionNumberMapper, metaclass=ABCMeta):
    """
    Mapper for `Sample` models.
    """
    pass


class StudyMapper(NamedMapper, InternalIDMapper, AccessionNumberMapper, metaclass=ABCMeta):
    """
    Mapper for `Study` models.
    """
    @abstractmethod
    def get_associated_with_sample(self, sample_internal_ids: str) -> Study:
        """
        Gets all the studies that the given samples (identified by ID) belong to.
        :param sample_internal_ids: the IDs of the samples that studies are to be got for
        :return: studies related to one or more of the given samples
        """
        pass


class LibraryMapper(NamedMapper, InternalIDMapper, metaclass=ABCMeta):
    """
    Mapper for `Library` models.
    """
    pass


class WellMapper(NamedMapper, InternalIDMapper, metaclass=ABCMeta):
    """
    Mapper for `Well` models.
    """
    pass


class MultiplexedLibraryMapper(NamedMapper, InternalIDMapper, metaclass=ABCMeta):
    """
    Mapper for `MultiplexedLibrary` models.
    """
    pass