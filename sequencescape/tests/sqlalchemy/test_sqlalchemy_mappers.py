import unittest
from abc import ABCMeta
from typing import List

from sequencescape.mappers import Mapper
from sequencescape.models import Sample, AccessionNumberModel, Model
from sequencescape.sqlalchemy._sqlalchemy_database_connector import SQLAlchemyDatabaseConnector
from sequencescape.sqlalchemy._sqlalchemy_mappers import SQLAlchemyMapper, SQLAlchemySampleMapper
from sequencescape.tests.model_stub_helpers import create_stub_sample, assign_unique_ids
from sequencescape.tests.sqlalchemy.stub_database import create_stub_database
from sequencescape.tests.test_mappers import MapperTest


class _SQLAlchemyMapperTest(MapperTest, metaclass=ABCMeta):
    """
    Base class of all tests for methods in SQLAlchemyMapper.
    """
    @staticmethod
    def create_mapper(mapper_type: type, model_type: type=None) -> SQLAlchemyMapper:
        """
        Creates a mapper for a given type of model that is setup to connect with a test database.
        :param mapper_type: the type of the mapper to create
        :param model_type: the type of model to be used with the mapper. Not required if mapper type dictates model.
        :return: the mapper for the given model, setup for use with a test database
        """
        connector, database_file_path = _SQLAlchemyMapperTest._create_connector()
        if mapper_type == SQLAlchemyMapper:
            return mapper_type(connector, model_type)
        else:
            return mapper_type(connector)

    @staticmethod
    def _create_connector() -> (SQLAlchemyDatabaseConnector, str):
        """
        Creates a connector to a test database.
        :return: connector to a test database
        """
        database_file_path, dialect = create_stub_database()
        connector = SQLAlchemyDatabaseConnector("%s:///%s" % (dialect, database_file_path))
        return connector, database_file_path


class TestAdd(_SQLAlchemyMapperTest):
    """
    Tests for `SQLAlchemyMapper.add`.
    """
    def test_add_with_none(self):
        mapper = _SQLAlchemyMapperTest.create_mapper(SQLAlchemyMapper, Model)
        self.assertRaises(ValueError, mapper.add, None)

    def test_add_with_non_model(self):
        mapper = _SQLAlchemyMapperTest.create_mapper(SQLAlchemyMapper, Model)
        self.assertRaises(ValueError, mapper.add, Mapper)

    def test_add_with_empty_list(self):
        model = create_stub_sample()

        mapper = _SQLAlchemyMapperTest.create_mapper(SQLAlchemyMapper, model.__class__)
        mapper.add([])

        retrieved_models = mapper.get_all()
        self.assertEqual(len(retrieved_models), 0)

    def test_add_with_model(self):
        model = create_stub_sample()

        mapper = _SQLAlchemyMapperTest.create_mapper(SQLAlchemyMapper, model.__class__)
        mapper.add(model)

        retrieved_models = mapper.get_all()
        self.assertEqual(len(retrieved_models), 1)
        self.assertEqual(retrieved_models[0], model)

    def test_add_with_model_list(self):
        models = assign_unique_ids([create_stub_sample(), create_stub_sample(), create_stub_sample()])

        mapper = _SQLAlchemyMapperTest.create_mapper(SQLAlchemyMapper, models[0].__class__)
        mapper.add(models)

        retrieved_models = mapper.get_all()
        self.assertCountEqual(retrieved_models, models)


class TestGetByName(_SQLAlchemyMapperTest):
    """
    Tests for `SQLAlchemyMapper.get_by_name`.
    """
    def test_get_by_name_with_name_of_non_existent(self):
        models = assign_unique_ids([create_stub_sample(), create_stub_sample()])

        self.check_get(
            SQLAlchemySampleMapper,
            models,
            [],
            lambda mapper: mapper.get_by_name("invalid"))

    def test_get_by_name_with_name(self):
        named_model = create_stub_sample()
        named_model.name = "expected_model"
        models = assign_unique_ids([create_stub_sample(), named_model, create_stub_sample()])  # type: List[NamedModel]

        self.check_get(
            SQLAlchemySampleMapper,
            models,
            [named_model],
            lambda mapper: mapper.get_by_name(named_model.name))

    def test_get_by_name_where_many_have_same_name(self):
        same_name = "test_name"
        names = [same_name, "test_other_name", same_name]
        models = assign_unique_ids([create_stub_sample(), create_stub_sample(), create_stub_sample()])  # type: List[NamedModel]
        for i in range(len(models)):
            models[i].name = names[i]

        self.check_get(
            SQLAlchemySampleMapper,
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_name(same_name)
        )

    def test_get_by_name_with_name_list(self):
        names = ["test_name1", "test_name2", "test_name3"]
        models = assign_unique_ids([create_stub_sample(), create_stub_sample(), create_stub_sample()])  # type: List[NamedModel]
        for i in range(len(models)):
            models[i].name = names[i]

        self.check_get(
            SQLAlchemySampleMapper,
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_name([models[0].name, models[2].name])
        )


class TestGetById(_SQLAlchemyMapperTest):
    """
    Tests for `SQLAlchemyMapper.get_by_id`.
    """
    def test_get_by_id_with_id_of_non_existent(self):
        models = assign_unique_ids([create_stub_sample(), create_stub_sample()])
        self.check_get(
            SQLAlchemySampleMapper,
            models,
            [],
            lambda mapper: mapper.get_by_id("invalid"))

    def test_get_by_id_with_id(self):
        models = assign_unique_ids([create_stub_sample(), create_stub_sample(), create_stub_sample()])
        self.check_get(
            SQLAlchemySampleMapper,
            models,
            [models[1]],
            lambda mapper: mapper.get_by_id(models[1].internal_id))

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

    def test_get_by_id_with_id_list(self):
        models = assign_unique_ids([create_stub_sample(), create_stub_sample(), create_stub_sample()])
        self.check_get(
            SQLAlchemySampleMapper,
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_id([models[0].internal_id, models[2].internal_id])
        )


class TestGetByAccessionNumber(_SQLAlchemyMapperTest):
    """
    Tests for `SQLAlchemyMapper.get_by_accession_number`.
    """
    _ACCESSION_NUMBERS = ["test_accession_number1", "test_accession_number2", "test_accession_number3"]

    def setUp(self):
        self.models = TestGetByAccessionNumber._create_accession_number_models_with_accession_numbers(
            TestGetByAccessionNumber._ACCESSION_NUMBERS)

    def test_get_by_accession_number_with_accession_number_of_non_existent(self):
        self.check_get(
            SQLAlchemySampleMapper,
            self.models,
            [],
            lambda mapper: mapper.get_by_accession_number("invalid"))

    def test_get_by_accession_number_with_accession_number(self):
        self.check_get(
            SQLAlchemySampleMapper,
            self.models,
            [self.models[1]],
            lambda mapper: mapper.get_by_accession_number(self.models[1].accession_number))

    def test_get_by_accession_number_with_accession_number_list(self):
        self.check_get(
            SQLAlchemySampleMapper,
            self.models,
            [self.models[0], self.models[2]],
            lambda mapper: mapper.get_by_accession_number([self.models[0].accession_number, self.models[2].accession_number])
        )

    def test_get_by_accession_number_where_many_have_same_accession_number(self):
        same_accession_number = TestGetByAccessionNumber._ACCESSION_NUMBERS[0]
        accession_numbers = [same_accession_number, TestGetByAccessionNumber._ACCESSION_NUMBERS[1], same_accession_number]
        models = TestGetByAccessionNumber._create_accession_number_models_with_accession_numbers(accession_numbers)

        self.check_get(
            SQLAlchemySampleMapper,
            models,
            [models[0], models[2]],
            lambda mapper: mapper.get_by_accession_number(same_accession_number)
        )

    @staticmethod
    def _create_accession_number_models_with_accession_numbers(accession_numbers: List[str]) -> List[AccessionNumberModel]:
        """
        TODO
        :param accession_numbers:
        :return:
        """
        models = [Sample(accession_number=accession_number) for accession_number in accession_numbers]
        assign_unique_ids(models)
        return models


if __name__ == '__main__':
    unittest.main()
