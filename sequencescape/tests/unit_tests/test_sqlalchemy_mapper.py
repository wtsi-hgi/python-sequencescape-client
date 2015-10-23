import unittest
import sqlite3

from sequencescape.sqlalchemy._sqlalchemy_database_connector import *
from sequencescape.sqlalchemy._sqlalchemy_mapper import SQLAlchemySampleMapper

from sequencescape.tests.unit_tests.setup_database import *
from sequencescape.model import *
from sequencescape.tests.unit_tests.mocks import *



class Test_SQLAlchemyMapper(unittest.TestCase):
    """
    TODO
    """
    def test__valid_add(self):
        database_file_path, dialect = create_database()

        sample = create_mock_sample()

        connector = SQLAlchemyDatabaseConnector("%s:///%s" % (dialect, database_file_path))
        sample_mapper = SQLAlchemySampleMapper(connector)
        sample_mapper.add(sample)

        connection = sqlite3.connect(database_file_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % convert_to_sqlalchemy_model(sample).__tablename__)
        results = cursor.fetchall()
        self.assertEquals(len(results), 1)

        result = [str(x) for x in list(results[0])]

        for property_name, value in vars(sample).items():
            self.assertIn(value, result)



if __name__ == '__main__':
    unittest.main()



