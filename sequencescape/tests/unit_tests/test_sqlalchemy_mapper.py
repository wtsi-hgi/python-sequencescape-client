import unittest
import sqlite3
from typing import Callable

from sequencescape.sqlalchemy._sqlalchemy_database_connector import *
from sequencescape.sqlalchemy._sqlalchemy_mapper import _SQLAlchemyMapper

from sequencescape.tests.unit_tests.setup_database import *
from sequencescape.model import *
from sequencescape.tests.unit_tests.mocks import *



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
        mapper = _SQLAlchemyMapper(connector, Sample)
        mapper.add(model)

        connection = sqlite3.connect(database_file_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % convert_to_sqlalchemy_model(model).__tablename__)
        results = cursor.fetchall()
        self.assertEquals(len(results), 1)

        result = [str(x) for x in list(results[0])]

        for property_name, value in vars(model).items():
            self.assertIn(value, result)

    def test_get_using_name_parameter(self):
        """
        TODO
        """
        named_model = create_mock_sample()
        self.__check_get(named_model, lambda mapper, model: mapper.get(name=model.name))

    def test_get_using_accession_number_parameter(self):
        """
        TODO
        """
        named_model = create_mock_sample()
        self.__check_get(named_model, lambda mapper, model: mapper.get(accession_number=model.accession_number))

    def test_get_using_internal_id_parameter(self):
        """
        TODO
        """
        named_model = create_mock_sample()
        self.__check_get(named_model, lambda mapper, model: mapper.get(internal_id=model.internal_id))

    def test_get_many_by_given_id(self):
        pass

    def __check_get(self, model: Model, mapper_get_function: Callable[[Mapper, Model], Model]):
        """
        TODO
        :param model:
        :param mapper_get_function:
        :return:
        """
        connector, database_file_path = Test_SQLAlchemyMapper.__create_connector()
        mapper = _SQLAlchemyMapper(connector, Sample)
        mapper.add(model)
        named_model_retrieved = mapper_get_function(mapper, model)

        # Not trusting object equality because does not use all properties
        for property_name, value in vars(named_model).items():
            self.assertEquals(str(named_model_retrieved.__dict__[property_name]), value)

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



