import unittest

from sequencescape.enums import Property
from sequencescape.tests.mock_mappers import MockMapper, MockNamedMapper, MockInternalIdMapper, \
    MockAccessionNumberMapper


class MapperTest(unittest.TestCase):
    """
    Tests on the abstract `Mapper` class.
    """
    def setUp(self):
        self._mapper = MockMapper()

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


class NamedMapperTest(MapperTest):
    _NAMES = ["test_name1", "test_name2", "test_name3"]

    def setUp(self):
        self._mapper = MockNamedMapper()

    def test_get_by_name_with_value(self):
        self._mapper.get_by_name(NamedMapperTest._NAMES[0])
        self._mapper.get_by_property_value(Property.NAME, NamedMapperTest._NAMES[0])

    def test_get_by_name_with_list(self):
        self._mapper.get_by_name(NamedMapperTest._NAMES)
        self._mapper._get_by_property_value_list(Property.NAME, NamedMapperTest._NAMES)


class InternalIdMapperTest(MapperTest):
    """
    TODO
    """
    _INTERNAL_IDS = [123, 456, 789]

    def setUp(self):
        self._mapper = MockInternalIdMapper()

    def test_get_by_id_with_value(self):
        self._mapper.get_by_id(InternalIdMapperTest._INTERNAL_IDS[0])
        self._mapper.get_by_property_value(Property.NAME, InternalIdMapperTest._INTERNAL_IDS[0])

    def test_get_by_id_with_list(self):
        self._mapper.get_by_id(InternalIdMapperTest._INTERNAL_IDS)
        self._mapper._get_by_property_value_list(Property.INTERNAL_ID, InternalIdMapperTest._INTERNAL_IDS)

    # TODO: Push this upwards to test Mapper superclass.
    # def test_get_by_id_where_many_have_same_id(self):
    #     same_id = 1
    #     ids = [same_id, 2, same_id]
    #     models = [create_mock_sample(), create_mock_sample(), create_mock_sample()]
    #     for i in range(len(models)):
    #         models[i].internal_id = ids[i]
    #
    #     mapper = self.create_mapper(Sample)
    #     self.assertRaises(ValueError, mapper.get_by_id, models[0].internal_id)


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
