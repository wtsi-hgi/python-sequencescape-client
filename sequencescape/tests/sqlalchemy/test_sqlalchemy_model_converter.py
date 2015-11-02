import unittest

from sequencescape.model import Sample, Study, Library, Well, MultiplexedLibrary, StudySamplesLink
from sequencescape.sqlalchemy._sqlalchemy_model import SQLAlchemySample, SQLAlchemyStudy, SQLAlchemyLibrary, \
    SQLAlchemyWell, SQLAlchemyMultiplexedLibrary, SQLAlchemyStudySamplesLink
from sequencescape.sqlalchemy._sqlalchemy_model_converter import get_equivalent_popo_model_type, \
    get_equivalent_sqlalchemy_model_type, convert_to_sqlalchemy_model, convert_to_popo_model
from sequencescape.tests.mocks import create_mock_sample, INTERNAL_ID, NAME, ACCESSION_NUMBER, ORGANISM, COMMON_NAME, \
    TAXON_ID, GENDER, ETHNICITY, COHORT, COUNTRY_OF_ORIGIN, GEOGRAPHICAL_REGION, IS_CURRENT, create_mock_study, \
    STUDY_TYPE, DESCRIPTION, STUDY_TITLE, STUDY_VISIBILITY, FACULTY_SPONSOR, create_mock_library, LIBRARY_TYPE, \
    create_mock_well, create_mock_multiplexed_library, create_mock_study_samples_link


class TestGetEquivalentPopoModelType(unittest.TestCase):
    """
    Unit testing for `get_equivalent_popo_model_type`.
    """
    def test_none_with_unsupported_type(self):
        self.assertIsNone(get_equivalent_popo_model_type(str))

    def test_correct_with_none(self):
        self.assertEqual(get_equivalent_popo_model_type(None), None)

    def test_correct_with_sample(self):
        self.assertEqual(get_equivalent_popo_model_type(SQLAlchemySample), Sample)

    def test_correct_with_study(self):
        self.assertEqual(get_equivalent_popo_model_type(SQLAlchemyStudy), Study)

    def test_correct_with_library(self):
        self.assertEqual(get_equivalent_popo_model_type(SQLAlchemyLibrary), Library)

    def test_correct_with_well(self):
        self.assertEqual(get_equivalent_popo_model_type(SQLAlchemyWell), Well)

    def test_correct_with_multiplexed_library(self):
        self.assertEqual(get_equivalent_popo_model_type(SQLAlchemyMultiplexedLibrary), MultiplexedLibrary)

    def test_correct_with_study_samples_link(self):
        self.assertEqual(get_equivalent_popo_model_type(SQLAlchemyStudySamplesLink), StudySamplesLink)


class TestGetEquivalentSqlalchemyModelType(unittest.TestCase):
    """
    Unit testing for `get_equivalent_sqlalchemy_model_type`.
    """
    def test_none_with_unsupported_type(self):
        self.assertIsNone(get_equivalent_sqlalchemy_model_type(str))

    def test_correct_with_none(self):
        self.assertEqual(get_equivalent_sqlalchemy_model_type(None), None)

    def test_correct_with_sample(self):
        self.assertEqual(get_equivalent_sqlalchemy_model_type(Sample), SQLAlchemySample)

    def test_correct_with_study(self):
        self.assertEqual(get_equivalent_sqlalchemy_model_type(Study), SQLAlchemyStudy)

    def test_correct_with_library(self):
        self.assertEqual(get_equivalent_sqlalchemy_model_type(Library), SQLAlchemyLibrary)

    def test_correct_with_well(self):
        self.assertEqual(get_equivalent_sqlalchemy_model_type(Well), SQLAlchemyWell)

    def test_correct_with_multiplexed_library(self):
        self.assertEqual(get_equivalent_sqlalchemy_model_type(MultiplexedLibrary), SQLAlchemyMultiplexedLibrary)

    def test_correct_with_study_samples_link(self):
        self.assertEqual(get_equivalent_sqlalchemy_model_type(StudySamplesLink), SQLAlchemyStudySamplesLink)


class TestConvertToSQLAlchemyModel(unittest.TestCase):
    """
    Unit testing for `convert_to_sqlalchemy_model`.
    """
    def test_convert_none(self):
        converted_model = convert_to_sqlalchemy_model(None)  # type: None
        self.assertIsNone(converted_model)

    def test_convert_sample(self):
        model = create_mock_sample()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemySample
        self.assertEqual(converted_model.__class__, SQLAlchemySample)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.accession_number, ACCESSION_NUMBER)
        self.assertEqual(converted_model.organism, ORGANISM)
        self.assertEqual(converted_model.common_name, COMMON_NAME)
        self.assertEqual(converted_model.taxon_id, TAXON_ID)
        self.assertEqual(converted_model.gender, GENDER)
        self.assertEqual(converted_model.ethnicity, ETHNICITY)
        self.assertEqual(converted_model.cohort, COHORT)
        self.assertEqual(converted_model.country_of_origin, COUNTRY_OF_ORIGIN)
        self.assertEqual(converted_model.geographical_region, GEOGRAPHICAL_REGION)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_study(self):
        model = create_mock_study()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyStudy
        self.assertEqual(converted_model.__class__, SQLAlchemyStudy)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.accession_number, ACCESSION_NUMBER)
        self.assertEqual(converted_model.study_type, STUDY_TYPE)
        self.assertEqual(converted_model.description, DESCRIPTION)
        self.assertEqual(converted_model.study_title, STUDY_TITLE)
        self.assertEqual(converted_model.study_visibility, STUDY_VISIBILITY)
        self.assertEqual(converted_model.faculty_sponsor, FACULTY_SPONSOR)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_library(self):
        model = create_mock_library()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyLibrary
        self.assertEqual(converted_model.__class__, SQLAlchemyLibrary)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.library_type, LIBRARY_TYPE)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_well(self):
        model = create_mock_well()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyWell
        self.assertEqual(converted_model.__class__, SQLAlchemyWell)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_multiplexed_library(self):
        model = create_mock_multiplexed_library()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyMultiplexedLibrary
        self.assertEqual(converted_model.__class__, SQLAlchemyMultiplexedLibrary)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_study_samples_link(self):
        model = create_mock_study_samples_link()
        converted_model = convert_to_sqlalchemy_model(model)  # type: SQLAlchemyStudySamplesLink
        self.assertEqual(converted_model.__class__, SQLAlchemyStudySamplesLink)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.is_current, IS_CURRENT)


class TestConvertToPopoModel(unittest.TestCase):
    """
    Unit testing for `convert_to_popo_model`.
    """
    def test_convert_none(self):
        converted_model = convert_to_popo_model(None)  # type: None
        self.assertIsNone(converted_model)

    def test_convert_sample(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_sample())
        converted_model = convert_to_popo_model(alchemy_model)  # type: Sample
        self.assertEqual(converted_model.__class__, Sample)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.accession_number, ACCESSION_NUMBER)
        self.assertEqual(converted_model.organism, ORGANISM)
        self.assertEqual(converted_model.common_name, COMMON_NAME)
        self.assertEqual(converted_model.taxon_id, TAXON_ID)
        self.assertEqual(converted_model.gender, GENDER)
        self.assertEqual(converted_model.ethnicity, ETHNICITY)
        self.assertEqual(converted_model.cohort, COHORT)
        self.assertEqual(converted_model.country_of_origin, COUNTRY_OF_ORIGIN)
        self.assertEqual(converted_model.geographical_region, GEOGRAPHICAL_REGION)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_study(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_study())
        converted_model = convert_to_popo_model(alchemy_model)  # type: Study
        self.assertEqual(converted_model.__class__, Study)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.accession_number, ACCESSION_NUMBER)
        self.assertEqual(converted_model.study_type, STUDY_TYPE)
        self.assertEqual(converted_model.description, DESCRIPTION)
        self.assertEqual(converted_model.study_title, STUDY_TITLE)
        self.assertEqual(converted_model.study_visibility, STUDY_VISIBILITY)
        self.assertEqual(converted_model.faculty_sponsor, FACULTY_SPONSOR)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_library(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_library())
        converted_model = convert_to_popo_model(alchemy_model)  # type: Library
        self.assertEqual(converted_model.__class__, Library)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.library_type, LIBRARY_TYPE)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_well(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_well())
        converted_model = convert_to_popo_model(alchemy_model)  # type: Well
        self.assertEqual(converted_model.__class__, Well)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_multiplexed_library(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_multiplexed_library())
        converted_model = convert_to_popo_model(alchemy_model)  # type: MultiplexedLibrary
        self.assertEqual(converted_model.__class__, MultiplexedLibrary)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.name, NAME)
        self.assertEqual(converted_model.is_current, IS_CURRENT)

    def test_convert_study_samples_link(self):
        alchemy_model = convert_to_sqlalchemy_model(create_mock_study_samples_link())
        converted_model = convert_to_popo_model(alchemy_model)  # type: StudySamplesLink
        self.assertEqual(converted_model.__class__, StudySamplesLink)
        self.assertEqual(converted_model.internal_id, INTERNAL_ID)
        self.assertEqual(converted_model.is_current, IS_CURRENT)


if __name__ == '__main__':
    unittest.main()
