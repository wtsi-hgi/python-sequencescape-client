from typing import Union, Any, List, Tuple
from unittest.mock import MagicMock

from sequencescape.enums import Property
from sequencescape.mappers import Mapper
from sequencescape.models import Model


class MockMapper(Mapper):
    def __init__(self):
        self.add = MagicMock()
        self.get_all = MagicMock()
        self._get_by_property_value_list = MagicMock()
        self._get_by_property_value_tuple = MagicMock()

    def get_all(self) -> List[Model]:
        return []

    def add(self, model: Union[Model, List[Model]]):
        pass

    def _get_by_property_value_list(self, property: Property, values: Union[Any, List[Any]]) -> List[Model]:
        return []

    def _get_by_property_value_tuple(
            self, property_value_tuples: Union[Tuple[Property, Any], List[Tuple[Property, Any]]]) -> List[Model]:
        return []
