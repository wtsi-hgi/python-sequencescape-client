import unittest
import sqlite3
from typing import Callable

from sequencescape.sqlalchemy._sqlalchemy_database_connector import *
from sequencescape.sqlalchemy._sqlalchemy_mapper import _SQLAlchemyMapper

from sequencescape.tests.unit_tests.setup_database import *
from sequencescape.model import *
from sequencescape.tests.unit_tests.mocks import *



# TODO: Generalise for use with any mapper implementation
class Test_SQLAlchemyMapper(unittest.TestCase):
    """
    TODO
    """
    def test_add_with_none(self):
        """
        TODO
        """
        connector = Test_SQLAlchemyMapper.__create_connector()
        mapper = _SQLAlchemyMapper(connector, Sample)
        self.assertRaises(ValueError, mapper.add, None)

    def test_add_with_non_model(self):
        """
        TODO
        """
        connector = Test_SQLAlchemyMapper.__create_connector()
        mapper = _SQLAlchemyMapper(connector, Sample)
        self.assertRaises(ValueError, mapper.add, SQLAlchemySample)

    def test_add_with_valid(self):
        """
        TODO
        """
        model = create_mock_sample()

        connector, database_file_path = Test_SQLAlchemyMapper.__create_connector()
        mapper = _SQLAlchemyMapper(connector, model.__class__)
        mapper.add(model)

        connection = sqlite3.connect(database_file_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % convert_to_sqlalchemy_model(model).__tablename__)
        results = cursor.fetchall()
        self.assertEquals(len(results), 1)

        result = [x for x in list(results[0])]

        for property_name, value in vars(model).items():
            self.assertIn(value, result)

    def test_add_all_with_empty(self):
        """
        TODO
        """
        model = create_mock_sample()

        connector, database_file_path = Test_SQLAlchemyMapper.__create_connector()
        mapper = _SQLAlchemyMapper(connector, model.__class__)
        mapper.add_all([])

        connection = sqlite3.connect(database_file_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % convert_to_sqlalchemy_model(model).__tablename__)
        results = cursor.fetchall()
        self.assertEquals(len(results), 0)

    def test_add_all_with_valid(self):
        """
        TODO
        """
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]

        connector, database_file_path = Test_SQLAlchemyMapper.__create_connector()
        mapper = _SQLAlchemyMapper(connector, models[0].__class__)
        mapper.add_all(models)

        connection = sqlite3.connect(database_file_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % convert_to_sqlalchemy_model(models[0]).__tablename__)
        results = cursor.fetchall()
        self.assertEquals(len(results), len(models))
        #TODO: Should make the test more extensive...

    def test_get_using_name_parameter(self):
        """
        TODO
        """
        named_model = create_mock_sample()
        named_model.name = "expected_model"
        models = [create_mock_sample(), named_model, create_mock_sample()]
        self.__check_get(
            models,
            named_model,
            lambda mapper: mapper.get(name=named_model.name))

    def test_get_using_accession_number_parameter(self):
        """
        TODO
        """
        accession_number_model = create_mock_sample()
        accession_number_model.accession_number = "EGAN00000000000"
        models = [create_mock_sample(), accession_number_model, create_mock_sample()]
        self.__check_get(
            models,
            accession_number_model,
            lambda mapper: mapper.get(accession_number=accession_number_model.accession_number))

    def test_get_using_internal_id_parameter(self):
        """
        TODO
        """
        internal_id_model = create_mock_sample()
        internal_id_model.internal_id = 5511223
        models = [create_mock_sample(), internal_id_model, create_mock_sample()]
        self.__check_get(
            models,
            internal_id_model,
            lambda mapper: mapper.get(internal_id=internal_id_model.internal_id))

    def test_get_many_by_name(self):
        """
        TODO
        """
        names = ["test_name1", "test_name2", "test_name3"]
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = i
            models[i].name = names[i]

        self.__check_get_many(
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_many_by_names([names[0], names[2]])
        )

    def test_get_many_by_internal_ids(self):
        """
        TODO
        """
        ids = [1, 2, 3]
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = ids[i]

        self.__check_get_many(
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_many_by_internal_ids([ids[0], ids[2]])
        )

    def test_get_many_by_accession_numbers(self):
        """
        TODO
        """
        accession_numbers = ["test_accession_number1", "test_accession_number2", "test_accession_number3"]
        models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
        for i in range(len(models)):
            models[i].internal_id = i
            models[i].accession_number = accession_numbers[i]

        self.__check_get_many(
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_many_by_accession_numbers([accession_numbers[0], accession_numbers[2]])
        )

    def __check_get(self, models: List[Model], expected_model: Model, mapper_get_function: Callable[[Mapper], Model]):
        """
        TODO
        :param model:
        :param mapper_get_function:
        :return:
        """
        self.__check_get_many(models, [expected_model], lambda mapper: [mapper_get_function(mapper)])

    def __check_get_many(
            self, models: List[Model], expected_models: List[Model], mapper_get: Callable[[Mapper], List[Model]]):
        """
        TODO
        :param model:
        :param mapper_get:
        :return:
        """
        model_type = None
        for model in models:
            if model_type is None:
                model_type = model.__class__
            elif model.__class__ != model_type:
                raise ValueError("All models must be of the same type")
        assert issubclass(model_type, Model)

        connector, database_file_path = Test_SQLAlchemyMapper.__create_connector()
        mapper = _SQLAlchemyMapper(connector, model_type)
        mapper.add_all(models)
        models_retrieved = mapper_get(mapper)
        self.assertEquals(len(models_retrieved), len(expected_models))

        for model_retrieved in models_retrieved:
            matched_model = [x for x in expected_models if x == model_retrieved]

            self.assertEquals(len(matched_model), 1, "If `0 != 1`, expected model was not retrieved from database")
            model = matched_model[0]

            # Check all properties (may be different to object equality)
            for property_name, value in vars(model).items():
                self.assertEquals(model_retrieved.__dict__[property_name], value, '`%s` mismatch' % property_name)

    @staticmethod
    def __create_connector() -> (SQLAlchemyDatabaseConnector, str):
        """
        TODO
        :return:
        """
        database_file_path, dialect = create_database()
        connector = SQLAlchemyDatabaseConnector("%s:///%s" % (dialect, database_file_path))
        return connector, database_file_path


if __name__ == '__main__':
    unittest.main()



