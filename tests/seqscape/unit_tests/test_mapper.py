import unittest
# from sequencescape.model import *
from sequencescape.sqlalchemy._sqlalchemy_mapper import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        connector = SQLAlchemyDatabaseConnector("host", 0, "database", "user")
        mapper = SQLAlchemyMapper(connector)
        mapper.get_one(name="abc")


if __name__ == '__main__':
    unittest.main()

