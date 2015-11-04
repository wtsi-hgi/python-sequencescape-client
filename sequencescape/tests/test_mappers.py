import unittest

from sequencescape.enums import Property
from sequencescape.tests.mock_mappers import MockMapper, MockNamedMapper, MockInternalIdMapper, \
    MockAccessionNumberMapper


class MapperTest(unittest.TestCase):
    """
    Tests on the abstract `Mapper` class.
    """
    _VALUES = ["test_value1", "test_value2", "test_value3"]

    def setUp(self):
        self._mapper = MockMapper()

    def test_get_by_property_value_with_value(self):
        self._mapper.get_by_property_value(Property.NAME, MapperTest._VALUES[0])
        self._mapper._get_by_property_value_list.assert_called_once_with(Property.NAME, [MapperTest._VALUES[0]])

    def test_get_by_property_value_with_list(self):
        self._mapper.get_by_property_value(Property.NAME, MapperTest._VALUES)
        self._mapper._get_by_property_value_list.assert_called_once_with(Property.NAME, MapperTest._VALUES)

    def test_get_by_property_value_with_tuple(self):
        property_value_tuple = (Property.NAME, MapperTest._VALUES[0])
        self._mapper.get_by_property_value(property_value_tuple)
        self._mapper._get_by_property_value_tuple.assert_called_once_with(property_value_tuple)

    def test_get_by_property_value_with_tuples_list(self):
        property_value_tuples = [
            (Property.NAME, MapperTest._VALUES[0]), (Property.ACCESSION_NUMBER, MapperTest._VALUES[1])]
        self._mapper.get_by_property_value(property_value_tuples)
        self._mapper._get_by_property_value_tuple.assert_called_once_with(property_value_tuples)


class NamedMapperTest(MapperTest):
    """
    TODO
    """
    _NAMES = ["test_name1", "test_name2", "test_name3"]

    def setUp(self):
        self._mapper = MockNamedMapper()

    def test_get_by_name_with_value(self):
        self._mapper.get_by_name(NamedMapperTest._NAMES[0])
        self._mapper._get_by_property_value_list.assert_called_once_with(Property.NAME, [NamedMapperTest._NAMES[0]])

    def test_get_by_name_with_list(self):
        self._mapper.get_by_name(NamedMapperTest._NAMES)
        self._mapper._get_by_property_value_list.assert_called_once_with(Property.NAME, NamedMapperTest._NAMES)


class InternalIdMapperTest(MapperTest):
    """
    TODO
    """
    _INTERNAL_IDS = [123, 456, 789]

    def setUp(self):
        self._mapper = MockInternalIdMapper()

    def test_get_by_id_with_value(self):
        self._mapper.get_by_id(InternalIdMapperTest._INTERNAL_IDS[0])
        self._mapper._get_by_property_value_list.assert_called_once_with(
            Property.INTERNAL_ID, [InternalIdMapperTest._INTERNAL_IDS[0]])

    def test_get_by_id_with_list(self):
        self._mapper.get_by_id(InternalIdMapperTest._INTERNAL_IDS)
        self._mapper._get_by_property_value_list.assert_called_once_with(
            Property.INTERNAL_ID, InternalIdMapperTest._INTERNAL_IDS)


class AccessionNumberMapperTest(MapperTest):
    """
    TODO
    """
    _ACCESSION_NUMBERS = ["test_accession_number1", "test_accession_number2", "test_accession_number3"]

    def setUp(self):
        self._mapper = MockAccessionNumberMapper()

    def test_get_by_accession_number_with_value(self):
        self._mapper.get_by_accession_number(AccessionNumberMapperTest._ACCESSION_NUMBERS[0])
        self._mapper.get_by_property_value(Property.NAME, AccessionNumberMapperTest._ACCESSION_NUMBERS[0])

    def test_get_by_accession_number_with_list(self):
        self._mapper.get_by_accession_number(AccessionNumberMapperTest._ACCESSION_NUMBERS)
        self._mapper._get_by_property_value_list(
            Property.ACCESSION_NUMBER, AccessionNumberMapperTest._ACCESSION_NUMBERS)


if __name__ == '__main__':
    unittest.main()
