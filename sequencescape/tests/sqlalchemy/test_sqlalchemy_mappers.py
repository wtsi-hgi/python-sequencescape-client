import unittest
from typing import List

from sequencescape import Property
from sequencescape._sqlalchemy.sqlalchemy_database_connector import SQLAlchemyDatabaseConnector
from sequencescape._sqlalchemy.sqlalchemy_mappers import SQLAlchemyMapper, SQLAlchemySampleMapper
from sequencescape.mappers import Mapper
from sequencescape.models import InternalIdModel
from sequencescape.tests.model_stub_helpers import create_stub_sample, assign_unique_ids
from sequencescape.tests.sqlalchemy.stub_database import create_stub_database


def _create_connector() -> (SQLAlchemyDatabaseConnector, str):
    """
    Creates a connector to a test database.
    :return: connector to a test database
    """
    database_file_path, dialect = create_stub_database()
    connector = SQLAlchemyDatabaseConnector("%s:///%s" % (dialect, database_file_path))
    return connector, database_file_path


class SQLAlchemyMapperTest(unittest.TestCase):
    """
    Tests for `SQLAlchemyMapper`.
    """
    def setUp(self):
        connector, database_location = _create_connector()
        self._mapper = SQLAlchemyMapper(connector, SQLAlchemyMapperTest._create_models(1)[0].__class__)

    def test_add_with_none(self):
        self.assertRaises(ValueError, self._mapper.add, None)

    def test_add_with_non_model(self):
        self.assertRaises(ValueError, self._mapper.add, Mapper)

    def test_add_with_empty_list(self):
        self._mapper.add([])

        retrieved_models = self._mapper.get_all()
        self.assertEqual(len(retrieved_models), 0)

    def test_add_with_model(self):
        model = self._create_models(1)[0]
        self._mapper.add(model)

        retrieved_models = self._mapper.get_all()
        self.assertEqual(len(retrieved_models), 1)
        self.assertEqual(retrieved_models[0], model)

    def test_add_with_model_list(self):
        models = self._create_models(5)
        self._mapper.add(models)

        retrieved_models = self._mapper.get_all()
        self.assertCountEqual(retrieved_models, models)

    def test__get_by_property_value_list_with_empty_list(self):
        models = self._create_models(5)
        models_to_retrieve = []
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_list(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models_to_retrieve))
        self.assertCountEqual(retrieved_models, models_to_retrieve)

    def test__get_by_property_value_list_with_list_of_existing(self):
        models = self._create_models(5)
        models_to_retrieve = [models[0], models[2]]
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_list(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models_to_retrieve))
        self.assertCountEqual(retrieved_models, models_to_retrieve)

    def test__get_by_property_value_list_with_list_of_non_existing(self):
        models = self._create_models(5)
        models_to_retrieve = [models.pop(), models.pop()]
        assert len(models) == 3
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_list(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models_to_retrieve))
        self.assertCountEqual(retrieved_models, [])

    def test__get_by_property_value_list_with_list_of_both_existing_and_non_existing(self):
        models = self._create_models(5)
        models_to_retrieve = [models[0], models[2], models.pop()]
        assert len(models) == 4
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_list(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models_to_retrieve))
        self.assertCountEqual(retrieved_models, models_to_retrieve[:2])

    def test__get_by_property_value_list_returns_correct_type(self):
        models = self._create_models(5)
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_list(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models))
        self.assertCountEqual(retrieved_models, models)
        self.assertIsInstance(retrieved_models[0], models[0].__class__)

    @staticmethod
    def _get_internal_ids(models: List[InternalIdModel]) -> List[int]:
        """
        Gets the ids of all of the given models.
        :param models: the models to get the ids of
        :return: the ids of the given models
        """
        return [model.internal_id for model in models]

    @staticmethod
    def _create_models(number_of_models: int) -> List[InternalIdModel]:
        """
        Creates a number of models to use in tests.
        :param number_of_models: the number of models to create
        :return: the models
        """
        return assign_unique_ids([create_stub_sample() for _ in range(number_of_models)])


class SQLAlchemySampleMapperTest(unittest.TestCase):
    """
    Tests for `SQLAlchemySampleMapper`.
    """
    def setUp(self):
        connector, database_location = _create_connector()
        self._mapper = SQLAlchemySampleMapper(connector)

    def test_get_associated_with_study_with_value(self):
        # TODO: Implement
        pass


class SQLAlchemyStudyMapperTest(unittest.TestCase):
    """
    Tests for `SQLAlchemyStudyMapper`.
    """
    def setUp(self):
        connector, database_location = _create_connector()
        self._mapper = SQLAlchemySampleMapper(connector)

    def test_get_associated_with_sample(self):
        # TODO: Implement
        pass


if __name__ == '__main__':
    unittest.main()
