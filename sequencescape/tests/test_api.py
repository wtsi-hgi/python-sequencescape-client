import unittest

from sequencescape import connect_to_sequencescape
from sequencescape.api import Connection
from sequencescape.mapper import Mapper
from sequencescape.tests.sqlalchemy.setup_database import create_database


class TestConnection(unittest.TestCase):
    """
    Tests for `Connection` class.
    """
    def test_with_valid_database_url(self):
        database_location, dialect = create_database()
        connect_to_sequencescape("%s:///%s" % (dialect, database_location))

    def test_with_no_database_url(self):
        self.assertRaises(ValueError, connect_to_sequencescape, "")

    def test_with_invalid_database_url(self):
        self.assertRaises(ValueError, connect_to_sequencescape, "dialect://host:invalid")

    def test_correct_mapper_properties(self):
        connection = Connection("dialect://host")
        self.assertIsInstance(connection.sample, Mapper)
        self.assertIsInstance(connection.study, Mapper)
        self.assertIsInstance(connection.multiplexed_library, Mapper)
        self.assertIsInstance(connection.library, Mapper)
        self.assertIsInstance(connection.well, Mapper)


class TestConnectToSequencescape(unittest.TestCase):
    """
    Tests for `connect_to_sequencescape` method.
    """
    def test_returns_connection(self):
        database_location = "dialect://host"
        connection = connect_to_sequencescape(database_location)
        self.assertIsInstance(connection, Connection)
        self.assertEquals(connection._database_location, database_location)


if __name__ == '__main__':
    unittest.main()
