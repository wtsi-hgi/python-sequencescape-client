import unittest
from typing import List

from sequencescape._sqlalchemy.sqlalchemy_database_connector import SQLAlchemyDatabaseConnector
from sequencescape._sqlalchemy.sqlalchemy_mappers import SQLAlchemyMapper, SQLAlchemySampleMapper, SQLAlchemyStudyMapper
from sequencescape.enums import Property
from sequencescape.mappers import Mapper
from sequencescape.models import InternalIdModel, Sample, Study
from sequencescape.tests._helpers import create_stub_sample, assign_unique_ids
from sequencescape.tests.sqlalchemy.stub_database import create_stub_database


def _create_connector() -> (SQLAlchemyDatabaseConnector, str):
    """
    Creates a connector to a test database.
    :return: connector to a test database
    """
    database_file_path, dialect = create_stub_database()
    connector = SQLAlchemyDatabaseConnector("%s:///%s" % (dialect, database_file_path))
    return connector, database_file_path


class SQLAlchemyMapperTest(unittest.TestCase):
    """
    Tests for `SQLAlchemyMapper`.
    """
    def setUp(self):
        connector, database_location = _create_connector()
        self._mapper = SQLAlchemyMapper(connector, SQLAlchemyMapperTest._create_models(1)[0].__class__)

    def test_add_with_none(self):
        self.assertRaises(ValueError, self._mapper.add, None)

    def test_add_with_non_model(self):
        self.assertRaises(ValueError, self._mapper.add, Mapper)

    def test_add_with_empty_list(self):
        self._mapper.add([])

        retrieved_models = self._mapper.get_all()
        self.assertEqual(len(retrieved_models), 0)

    def test_add_with_model(self):
        model = self._create_models(1)[0]
        self._mapper.add(model)

        retrieved_models = self._mapper.get_all()
        self.assertEqual(len(retrieved_models), 1)
        self.assertEqual(retrieved_models[0], model)

    def test_add_with_model_list(self):
        models = self._create_models(5)
        self._mapper.add(models)

        retrieved_models = self._mapper.get_all()
        self.assertCountEqual(retrieved_models, models)

    def test__get_by_property_value_list_with_empty_list(self):
        models = self._create_models(5)
        models_to_retrieve = []
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_sequence(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models_to_retrieve))
        self.assertCountEqual(retrieved_models, models_to_retrieve)

    def test__get_by_property_value_list_with_list_of_existing(self):
        models = self._create_models(5)
        models_to_retrieve = [models[0], models[2]]
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_sequence(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models_to_retrieve))
        self.assertCountEqual(retrieved_models, models_to_retrieve)

    def test__get_by_property_value_list_with_list_of_non_existing(self):
        models = self._create_models(5)
        models_to_retrieve = [models.pop(), models.pop()]
        assert len(models) == 3
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_sequence(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models_to_retrieve))
        self.assertCountEqual(retrieved_models, [])

    def test__get_by_property_value_list_with_list_of_both_existing_and_non_existing(self):
        models = self._create_models(5)
        models_to_retrieve = [models[0], models[2], models.pop()]
        assert len(models) == 4
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_sequence(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models_to_retrieve))
        self.assertCountEqual(retrieved_models, models_to_retrieve[:2])

    def test__get_by_property_value_list_returns_correct_type(self):
        models = self._create_models(5)
        self._mapper.add(models)

        retrieved_models = self._mapper._get_by_property_value_sequence(
            Property.INTERNAL_ID, SQLAlchemyMapperTest._get_internal_ids(models))
        self.assertCountEqual(retrieved_models, models)
        self.assertIsInstance(retrieved_models[0], models[0].__class__)

    @staticmethod
    def _get_internal_ids(models: List[InternalIdModel]) -> List[int]:
        """
        Gets the ids of all of the given models.
        :param models: the models to get_by_path the ids of
        :return: the ids of the given models
        """
        return [model.internal_id for model in models]

    @staticmethod
    def _create_models(number_of_models: int) -> List[InternalIdModel]:
        """
        Creates a number of models to use in tests.
        :param number_of_models: the number of models to create
        :return: the models
        """
        return assign_unique_ids([create_stub_sample() for _ in range(number_of_models)])


class SQLAssociationMapperTest(unittest.TestCase):
    """
    Tests for `SQLAssociationMapper`.

    Tested through `SQLAlchemySampleMapper`.
    """
    _STUDY_INTERNAL_IDS = [123, 456]
    _SAMPLE_INTERNAL_IDS = [789, 101112]

    def setUp(self):
        connector, database_location = _create_connector()
        self._sample_mapper = SQLAlchemySampleMapper(connector)
        self._study_mapper = SQLAlchemyStudyMapper(connector)

    def test__get_associated_with_non_existent_study(self):
        self.assertRaises(ValueError, self._sample_mapper.get_associated_with_study, Study())

    def test__get_associated_with_non_associated(self):
        study = Study(internal_id=SQLAssociationMapperTest._STUDY_INTERNAL_IDS[0])
        self._study_mapper.add(study)

        associated_samples = self._sample_mapper.get_associated_with_study(study)
        self.assertEquals(len(associated_samples), 0)

    def test__get_associated_with_value(self):
        study = Study(internal_id=SQLAssociationMapperTest._STUDY_INTERNAL_IDS[0])
        self._study_mapper.add(study)

        samples = [
            Sample(internal_id=SQLAssociationMapperTest._SAMPLE_INTERNAL_IDS[0]),
            Sample(internal_id=SQLAssociationMapperTest._SAMPLE_INTERNAL_IDS[1])
        ]
        self._sample_mapper.add(samples)

        self._sample_mapper.set_association_with_study(samples, study)
        self.assertEquals(self._study_mapper.get_by_id(study.internal_id)[0], study)

        associated_samples = self._sample_mapper.get_associated_with_study(study)
        self.assertCountEqual(associated_samples, samples)

    def test__get_associated_with_list(self):
        studies = [
            Study(internal_id=SQLAssociationMapperTest._STUDY_INTERNAL_IDS[0]),
            Study(internal_id=SQLAssociationMapperTest._STUDY_INTERNAL_IDS[1])
        ]
        self._study_mapper.add(studies)

        samples = [
            Sample(internal_id=SQLAssociationMapperTest._SAMPLE_INTERNAL_IDS[0]),
            Sample(internal_id=SQLAssociationMapperTest._SAMPLE_INTERNAL_IDS[1])
        ]
        self._sample_mapper.add(samples)

        self._sample_mapper.set_association_with_study(samples[0], studies[0])
        self._sample_mapper.set_association_with_study(samples[1], studies[1])

        associated_samples = self._sample_mapper.get_associated_with_study(studies)
        self.assertCountEqual(associated_samples, samples)

    def test__get_associated_with_list_and_shared_assocaition(self):
        studies = [
            Study(internal_id=SQLAssociationMapperTest._STUDY_INTERNAL_IDS[0]),
            Study(internal_id=SQLAssociationMapperTest._STUDY_INTERNAL_IDS[1])
        ]
        self._study_mapper.add(studies)

        sample = Sample(internal_id=SQLAssociationMapperTest._SAMPLE_INTERNAL_IDS[0])
        self._sample_mapper.add(sample)

        self._sample_mapper.set_association_with_study(sample, studies[0])
        self._sample_mapper.set_association_with_study(sample, studies[1])

        associated_samples = self._sample_mapper.get_associated_with_study(studies)
        self.assertCountEqual(associated_samples, [sample])


if __name__ == "__main__":
    unittest.main()
