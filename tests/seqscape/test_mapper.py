import unittest
from sequencescape.model import *
from sequencescape._mapper import *
from sequencescape.database_connector import DummyDatabaseConnector


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mapper = Mapper(DummyDatabaseConnector())
        mapper.get_database_connector().create_session()


if __name__ == '__main__':
    unittest.main()

