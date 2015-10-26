import unittest

from sequencescape.sqlalchemy._sqlalchemy_model_converter import *
from sequencescape.tests.mocks import *


class TestGetEquivalentPopoModelType(unittest.TestCase):
    """
    Unit tests for `get_equivalent_popo_model_type`.
    """
    def test_none_with_unsupported_type(self):
        self.assertIsNone(get_equivalent_popo_model_type(str))

    def test_correct_with_sample(self):
        self.assertEquals(get_equivalent_popo_model_type(SQLAlchemySample), Sample)

    def test_correct_with_study(self):
        self.assertEquals(get_equivalent_popo_model_type(SQLAlchemyStudy), Study)

    def test_correct_with_library(self):
        self.assertEquals(get_equivalent_popo_model_type(SQLAlchemyLibrary), Library)

    def test_correct_with_well(self):
        self.assertEquals(get_equivalent_popo_model_type(SQLAlchemyWell), Well)

    def test_correct_with_multiplexed_library(self):
        self.assertEquals(get_equivalent_popo_model_type(SQLAlchemyMultiplexedLibrary), MultiplexedLibrary)

    def test_correct_with_study_samples_link(self):
        self.assertEquals(get_equivalent_popo_model_type(SQLAlchemyStudySamplesLink), StudySamplesLink)


class TestGetEquivalentSqlalchemyModelType(unittest.TestCase):
    """
    Unit tests for `get_equivalent_sqlalchemy_model_type`.
    """
    def test_none_with_unsupported_type(self):
        self.assertIsNone(get_equivalent_sqlalchemy_model_type(str))

    def test_correct_with_sample(self):
        self.assertEquals(get_equivalent_sqlalchemy_model_type(Sample), SQLAlchemySample)

    def test_correct_with_study(self):
        self.assertEquals(get_equivalent_sqlalchemy_model_type(Study), SQLAlchemyStudy)

    def test_correct_with_library(self):
        self.assertEquals(get_equivalent_sqlalchemy_model_type(Library), SQLAlchemyLibrary)

    def test_correct_with_well(self):
        self.assertEquals(get_equivalent_sqlalchemy_model_type(Well), SQLAlchemyWell)

    def test_correct_with_multiplexed_library(self):
        self.assertEquals(get_equivalent_sqlalchemy_model_type(MultiplexedLibrary), SQLAlchemyMultiplexedLibrary)

    def test_correct_with_study_samples_link(self):
        self.assertEquals(get_equivalent_sqlalchemy_model_type(StudySamplesLink), SQLAlchemyStudySamplesLink)


class TestConvertToSQLAlchemyModel(unittest.TestCase):
    """
    Unit tests for `convert_to_sqlalchemy_model`.
    """
    def test_convert_sample(self):
        model = create_mock_sample()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemySample
        self.assertEquals(converted_model.__class__, SQLAlchemySample)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.accession_number, ACCESSION_NUMBER)
        self.assertEquals(converted_model.organism, ORGANISM)
        self.assertEquals(converted_model.common_name, COMMON_NAME)
        self.assertEquals(converted_model.taxon_id, TAXON_ID)
        self.assertEquals(converted_model.gender, GENDER)
        self.assertEquals(converted_model.ethnicity, ETHNICITY)
        self.assertEquals(converted_model.cohort, COHORT)
        self.assertEquals(converted_model.country_of_origin, COUNTRY_OF_ORIGIN)
        self.assertEquals(converted_model.geographical_region, GEOGRAPHICAL_REGION)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_study(self):
        model = create_mock_study()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyStudy
        self.assertEquals(converted_model.__class__, SQLAlchemyStudy)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.accession_number, ACCESSION_NUMBER)
        self.assertEquals(converted_model.study_type, STUDY_TYPE)
        self.assertEquals(converted_model.description, DESCRIPTION)
        self.assertEquals(converted_model.study_title, STUDY_TITLE)
        self.assertEquals(converted_model.study_visibility, STUDY_VISIBILITY)
        self.assertEquals(converted_model.faculty_sponsor, FACULTY_SPONSOR)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_library(self):
        model = create_mock_library()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyLibrary
        self.assertEquals(converted_model.__class__, SQLAlchemyLibrary)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.library_type, LIBRARY_TYPE)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_well(self):
        model = create_mock_well()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyWell
        self.assertEquals(converted_model.__class__, SQLAlchemyWell)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_multiplexed_library(self):
        model = create_mock_multiplexed_library()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyMultiplexedLibrary
        self.assertEquals(converted_model.__class__, SQLAlchemyMultiplexedLibrary)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_study_samples_link(self):
        model = create_mock_study_samples_link()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyStudySamplesLink
        self.assertEquals(converted_model.__class__, SQLAlchemyStudySamplesLink)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.is_current, IS_CURRENT)


class TestConvertToPopoModel(unittest.TestCase):
    """
    Unit tests for `convert_to_popo_model`.
    """
    def test_convert_sample(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_sample())
        converted_model = convert_to_popo_model(alchemy_model)  # type: Sample
        self.assertEquals(converted_model.__class__, Sample)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.accession_number, ACCESSION_NUMBER)
        self.assertEquals(converted_model.organism, ORGANISM)
        self.assertEquals(converted_model.common_name, COMMON_NAME)
        self.assertEquals(converted_model.taxon_id, TAXON_ID)
        self.assertEquals(converted_model.gender, GENDER)
        self.assertEquals(converted_model.ethnicity, ETHNICITY)
        self.assertEquals(converted_model.cohort, COHORT)
        self.assertEquals(converted_model.country_of_origin, COUNTRY_OF_ORIGIN)
        self.assertEquals(converted_model.geographical_region, GEOGRAPHICAL_REGION)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_study(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_study())
        converted_model = convert_to_popo_model(alchemy_model)  # type: Study
        self.assertEquals(converted_model.__class__, Study)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.accession_number, ACCESSION_NUMBER)
        self.assertEquals(converted_model.study_type, STUDY_TYPE)
        self.assertEquals(converted_model.description, DESCRIPTION)
        self.assertEquals(converted_model.study_title, STUDY_TITLE)
        self.assertEquals(converted_model.study_visibility, STUDY_VISIBILITY)
        self.assertEquals(converted_model.faculty_sponsor, FACULTY_SPONSOR)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_library(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_library())
        converted_model = convert_to_popo_model(alchemy_model)  # type: Library
        self.assertEquals(converted_model.__class__, Library)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.library_type, LIBRARY_TYPE)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_well(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_well())
        converted_model = convert_to_popo_model(alchemy_model)  # type: Well
        self.assertEquals(converted_model.__class__, Well)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_multiplexed_library(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_multiplexed_library())
        converted_model = convert_to_popo_model(alchemy_model)  # type: MultiplexedLibrary
        self.assertEquals(converted_model.__class__, MultiplexedLibrary)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.name, NAME)
        self.assertEquals(converted_model.is_current, IS_CURRENT)

    def test_convert_study_samples_link(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_study_samples_link())
        converted_model = convert_to_popo_model(alchemy_model)  # type: StudySamplesLink
        self.assertEquals(converted_model.__class__, StudySamplesLink)
        self.assertEquals(converted_model.internal_id, INTERNAL_ID)
        self.assertEquals(converted_model.is_current, IS_CURRENT)


if __name__ == '__main__':
    unittest.main()
