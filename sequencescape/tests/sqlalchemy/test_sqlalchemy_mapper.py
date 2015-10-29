import unittest
from typing import Callable, List, Union

from sequencescape.mapper import Mapper
from sequencescape.model import Sample, Model
from sequencescape.sqlalchemy._sqlalchemy_database_connector import SQLAlchemyDatabaseConnector
from sequencescape.sqlalchemy._sqlalchemy_mapper import SQLAlchemyMapper
from sequencescape.tests.mocks import create_mock_sample
from sequencescape.tests.sqlalchemy.setup_database import create_database


class _TestSQLAlchemyMapper(unittest.TestCase):
    """
    Base class of all tests for methods in SQLAlchemyMapper.
    """
    def _check_get(self, models: List[Model], expected_model: Union[Model, None], mapper_get_function: Callable[[Mapper], Model]):
        """
        Checks that when the given models are inserted into a database, the mapper gets the given expected model back
        when it uses the given mapper get function.
        :param models: the models that should be in the database. Each model should have a unique internal_id
        :param expected_model: the model to expect to be returned with the mapper get function
        :param mapper_get_function: function that takes the mapper and invokes the get method under test
        """
        self._check_get_many(models, [expected_model], lambda mapper: [mapper_get_function(mapper)])

    def _check_get_many(
            self, models: List[Model], expected_models: List[Union[Model, None]], mapper_get: Callable[[Mapper], List[Model]]):
        """
        Checks that when the given models are inserted into a database, the mapper gets the given expected models back
        when it uses the given mapper get function.
        :param models: the models that should be in the database. Each model should have a unique internal_id
        :param expected_model: the models to expect to be returned with the mapper get function
        :param mapper_get_function: function that takes the mapper and invokes the get method under test
        """
        model_type = None
        for model in models:
            if model_type is None:
                model_type = model.__class__
            elif model.__class__ != model_type:
                raise ValueError("All models must be of the same type")
        assert issubclass(model_type, Model)

        mapper = _TestSQLAlchemyMapper._create_mapper(model_type)
        mapper.add(models)
        models_retrieved = mapper_get(mapper)
        self.assertEqual(len(models_retrieved), len(expected_models))

        for model_retrieved in models_retrieved:
            matched_models = [x for x in expected_models if x == model_retrieved]

            self.assertEqual(len(matched_models), 1, "If `0 != 1`, expected model was not retrieved from database")
            model = matched_models[0]

            if model is not None:
                # Check all properties (may be different to object equality)
                for property_name, value in vars(model).items():
                    self.assertEqual(model_retrieved.__dict__[property_name], value, '`%s` mismatch' % property_name)

    @staticmethod
    def _create_mapper(model_type: type) -> SQLAlchemyMapper:
        """
        Creates a mapper for a given type of model that is setup to connect with a test database.
        :param model_type: the type of model to create a mapper for
        :return: the mapper for the given model, setup for use with a test database
        """
        connector, database_file_path = _TestSQLAlchemyMapper._create_connector()
        return SQLAlchemyMapper(connector, model_type)

    @staticmethod
    def _create_connector() -> (SQLAlchemyDatabaseConnector, str):
        """
        Creates a connector to a test database.
        :return: connector to a test database
        """
        database_file_path, dialect = create_database()
        connector = SQLAlchemyDatabaseConnector("%s:///%s" % (dialect, database_file_path))
        return connector, database_file_path


class TestAdd(_TestSQLAlchemyMapper):
    """
    Tests for `SQLAlchemyMapper.add`.
    """
    def test_add_with_none(self):
        mapper = _TestSQLAlchemyMapper._create_mapper(Sample)
        self.assertRaises(ValueError, mapper.add, None)

    def test_add_with_non_model(self):
        mapper = _TestSQLAlchemyMapper._create_mapper(Sample)
        self.assertRaises(ValueError, mapper.add, Mapper)

    def test_add_with_empty_list(self):
        model = create_mock_sample()

        mapper = _TestSQLAlchemyMapper._create_mapper(model.__class__)
        mapper.add([])

        retrieved_models = mapper.get_all()
        self.assertEqual(len(retrieved_models), 0)

    def test_add_with_model(self):
        model = create_mock_sample()

        mapper = _TestSQLAlchemyMapper._create_mapper(model.__class__)
        mapper.add(model)

        retrieved_models = mapper.get_all()
        self.assertEqual(len(retrieved_models), 1)
        self.assertEqual(retrieved_models[0], model)

    def test_add_with_model_list(self):
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = i

        mapper = _TestSQLAlchemyMapper._create_mapper(models[0].__class__)
        mapper.add(models)

        retrieved_models = mapper.get_all()
        self.assertEqual(len(retrieved_models), len(models))
        for retrieved_model in retrieved_models:
            self.assertIn(retrieved_model, models)


class TestGetByName(_TestSQLAlchemyMapper):
    """
    Tests for `SQLAlchemyMapper.get_by_name`.
    """
    def test_get_by_name_with_name_of_non_existent(self):
        models = [create_mock_sample(), create_mock_sample()]
        self._check_get(
            models,
            None,
            lambda mapper: mapper.get_by_name("invalid"))

    def test_get_by_name_with_name(self):
        named_model = create_mock_sample()
        named_model.name = "expected_model"
        models = [create_mock_sample(), named_model, create_mock_sample()]
        self._check_get(
            models,
            named_model,
            lambda mapper: mapper.get_by_name(named_model.name))

    def test_get_by_name_with_name_list(self):
        names = ["test_name1", "test_name2", "test_name3"]
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = i
            models[i].name = names[i]

        self._check_get_many(
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_name([names[0], names[2]])
        )


class TestGetById(_TestSQLAlchemyMapper):
    """
    Tests for `SQLAlchemyMapper.get_by_id`.
    """
    def test_get_by_id_with_id_of_non_existent(self):
        models = [create_mock_sample(), create_mock_sample()]
        self._check_get(
            models,
            None,
            lambda mapper: mapper.get_by_id("invalid"))

    def test_get_by_id_with_id(self):
        internal_id_model = create_mock_sample()
        internal_id_model.internal_id = 5511223
        models = [create_mock_sample(), internal_id_model, create_mock_sample()]
        self._check_get(
            models,
            internal_id_model,
            lambda mapper: mapper.get_by_id(internal_id_model.internal_id))

    def test_get_by_id_with_id_list(self):
        ids = [1, 2, 3]
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = ids[i]

        self._check_get_many(
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_id([ids[0], ids[2]])
        )


class TestGetByAccessionNumber(_TestSQLAlchemyMapper):
    """
    Tests for `SQLAlchemyMapper.get_by_accession_number`.
    """
    def test_get_by_accession_number_with_accession_number_of_non_existent(self):
        models = [create_mock_sample(), create_mock_sample()]
        self._check_get(
            models,
            None,
            lambda mapper: mapper.get_by_accession_number("invalid"))

    def test_get_by_accession_number_with_accession_number(self):
        accession_number_model = create_mock_sample()
        accession_number_model.accession_number = "EGAN00000000000"
        models = [create_mock_sample(), accession_number_model, create_mock_sample()]
        self._check_get(
            models,
            accession_number_model,
            lambda mapper: mapper.get_by_accession_number(accession_number_model.accession_number))

    def test_get_by_accession_number_with_accession_number_list(self):
        accession_numbers = ["test_accession_number1", "test_accession_number2", "test_accession_number3"]
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = i
            models[i].accession_number = accession_numbers[i]

        self._check_get_many(
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_accession_number([accession_numbers[0], accession_numbers[2]])
        )


class TestGetByPropertyValue(_TestSQLAlchemyMapper):
    """
    Tests for `SQLAlchemyMapper.get_by_property_value`.
    """
    def test_get_by_property_value_with_property_value_of_non_existent(self):
        models = [create_mock_sample(), create_mock_sample()]
        self._check_get(
            models,
            None,
            lambda mapper: mapper.get_by_property_value("name", "invalid"))

    def test_get_by_property_value_with_property_value(self):
        named_model = create_mock_sample()
        named_model.name = "expected_model"
        models = [create_mock_sample(), named_model, create_mock_sample()]
        self._check_get(
            models,
            named_model,
            lambda mapper: mapper.get_by_property_value("name", named_model.name))

    def test_get_by_property_value_with_property_value_list(self):
        names = ["test_name1", "test_name2", "test_name3"]
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = i
            models[i].name = names[i]

        self._check_get_many(
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_property_value("name", [names[0], names[2]])
        )

    def test_get_by_property_value_with_property_tuples_of_different_properties(self):
        names = ["test_name1", "test_name2", "test_name3"]
        accession_numbers = ["test_accession_number1", "test_accession_number2", "test_accession_number3"]
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = i + 1
            models[i].name = names[i]
            models[i].accession_number = accession_numbers[i]

        self._check_get_many(
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_property_value([("name", names[0]), ("accession_number", accession_numbers[2])])
        )


if __name__ == '__main__':
    unittest.main()
