from typing import Union, Any, List, Tuple
from unittest.mock import MagicMock

from sequencescape.enums import Property
from sequencescape.mappers import Mapper, NamedMapper, InternalIdMapper, AccessionNumberMapper, SampleMapper, WellMapper, \
    MultiplexedLibraryMapper, LibraryMapper, StudyMapper
from sequencescape.models import Model


class MockMapper(Mapper):
    def __init__(self):
        self.add = MagicMock()
        self.get_all = MagicMock(return_value=[])
        self._get_by_property_value_list = MagicMock(return_value=[])
        self._get_by_property_value_tuple = MagicMock(return_value=[])

    def get_all(self) -> List[Model]:
        pass

    def add(self, model: Union[Model, List[Model]]):
        pass

    def _get_by_property_value_list(self, property: Property, values: Union[Any, List[Any]]) -> List[Model]:
        pass

    def _get_by_property_value_tuple(
            self, property_value_tuples: Union[Tuple[Property, Any], List[Tuple[Property, Any]]]) -> List[Model]:
        pass


class MockNamedMapper(MockMapper, NamedMapper):
    def __init__(self):
        super(self.__class__, self).__init__()


class MockInternalIdMapper(MockMapper, InternalIdMapper):
    def __init__(self):
        super(self.__class__, self).__init__()


class MockAccessionNumberMapper(MockMapper, AccessionNumberMapper):
    def __init__(self):
        super(self.__class__, self).__init__()


class MockSampleMapper(MockMapper, SampleMapper):
    def __init__(self):
        super(self.__class__, self).__init__()


class MockStudyMapper(MockMapper, StudyMapper):
    def __init__(self):
        super(self.__class__, self).__init__()


class MockLibraryMapper(MockMapper, LibraryMapper):
    def __init__(self):
        super(self.__class__, self).__init__()


class MockMultiplexedLibraryMapper(MockMapper, MultiplexedLibraryMapper):
    def __init__(self):
        super(self.__class__, self).__init__()


class MockWellMapper(MockMapper, WellMapper):
    def __init__(self):
        super(self.__class__, self).__init__()
