import unittest
from abc import ABCMeta, abstractmethod
from typing import List, Callable, Any, cast

from sequencescape.enums import Property
from sequencescape.mappers import Mapper
from sequencescape.models import Model, InternalIdModel
from sequencescape.tests.mock_mappers import MockMapper


class MapperTest(unittest.TestCase, metaclass=ABCMeta):
    """
    Base class of all tests for methods in `Mapper`.
    """
    @staticmethod
    @abstractmethod
    def create_mapper(mapper_type: type=None, model_type: type=None) -> Mapper:
        """
        Creates a mapper for a given type of model that is setup with a test data source
        :param mapper_type: the type of the mapper to create
        :param model_type: the type of model to be used with the mapper. Not required if mapper type dictates model
        :return: the mapper for the given model
        """
        pass

    def check_get(self, mapper_type: type, models: List[Model], expected_models: List[Model],
                  mapper_get: Callable[[Mapper], List[Model]]):
        """
        Checks that when the given models are inserted into a database, the mapper gets the given expected models back
        when it uses the given mapper get function.
        :param mapper_type: the type of mapper to test get with
        :param models: the models that should be in the database. Each model should have a unique internal_id
        :param expected_model: the models to expect to be returned with the mapper get function
        :param mapper_get_function: function that takes the mapper and invokes the get method under test
        """
        if mapper_type == Mapper:
            # XXX: Can't use it with lots of classes...
            raise ValueError("Cannot use this helper with abstract `Mapper` class")

        model_type = None
        for model in models:
            if model_type is None:
                model_type = model.__class__
            elif model.__class__ != model_type:
                raise ValueError("All models must be of the same type")
        assert issubclass(model_type, Model)

        if isinstance(model_type, InternalIdModel):
            internal_ids = [cast(x, InternalIdModel).internal_id for x in models]
            if len(internal_ids) != len(set(internal_ids)):
                raise ValueError("Cannot add models to database with duplicate IDs")

        mapper = self.create_mapper(mapper_type, model_type)
        assert mapper.__class__ == mapper_type
        mapper.add(models)
        self.assertCountEqual(mapper.get_all(), models, "Mapper did not add models correctly")
        models_retrieved = mapper_get(mapper)
        self.assertCountEqual(models_retrieved, expected_models)


class TestAbstractMapper(MapperTest):
    """
    Tests on the abstract `Mapper` class.
    """
    def setUp(self):
        self._mapper = self.create_mapper()

    def test_get_by_property_value_with_value(self):
        name = "test_name"
        self._mapper.get_by_property_value(Property.NAME, name)
        self._mapper._get_by_property_value_list.assert_called_once_with(Property.NAME, [name])

    def test_get_by_property_value_with_list(self):
        names = ["test_name1", "test_name2", "test_name3"]
        self._mapper.get_by_property_value(Property.NAME, names)
        self._mapper._get_by_property_value_list.assert_called_once_with(Property.NAME, names)

    def test_get_by_property_value_with_tuple(self):
        property_value_tuple = (Property.NAME, "test_name")
        self._mapper.get_by_property_value(property_value_tuple)
        self._mapper._get_by_property_value_tuple.assert_called_once_with(property_value_tuple)

    def test_get_by_property_value_with_tuples_list(self):
        property_value_tuples = [(Property.NAME, "test_name1"), (Property.ACCESSION_NUMBER, "test_accession_number1")]
        self._mapper.get_by_property_value(property_value_tuples)
        self._mapper._get_by_property_value_tuple.assert_called_once_with(property_value_tuples)

    @staticmethod
    def create_mapper(mapper_type: type=None, model_type: type=None):
        return MockMapper()


if __name__ == '__main__':
    unittest.main()