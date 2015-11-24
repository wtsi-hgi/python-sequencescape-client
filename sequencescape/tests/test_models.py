import unittest

from sequencescape import InternalIdModel, AccessionNumberModel, IsCurrentModel, Sample, Study, Library
from sequencescape import NamedModel
from sequencescape.tests.model_stub_helpers import COMMON_NAME, GENDER, ETHNICITY, COHORT, COUNTRY_OF_ORIGIN, \
    GEOGRAPHICAL_REGION, STUDY_TYPE, DESCRIPTION, STUDY_TITLE, STUDY_VISIBILITY, FACULTY_SPONSOR, LIBRARY_TYPE
from sequencescape.tests.model_stub_helpers import ORGANISM, TAXON_ID


class _TestNamedModel(unittest.TestCase):
    """
    Tests for `NamedModel`.
    """
    class _MockNamedModel(NamedModel):
        pass

    def test_not_equal_if_different_name(self):
        model1 = _TestNamedModel._MockNamedModel()
        model1.name = "this"
        model2 = _TestNamedModel._MockNamedModel()
        model2.name = "that"
        self.assertNotEqual(model1, model2)

    def test_can_set_name_with_named_parameter(self):
        name = "test_name"
        model = _TestNamedModel._MockNamedModel(name=name)
        self.assertEquals(model.name, name)


class _TestInternalIdModel(unittest.TestCase):
    """
    Tests for `InternalIdModel`.
    """
    class _MockInternalIdModel(InternalIdModel):
        pass

    def test_not_equal_if_different_id(self):
        model1 = _TestInternalIdModel._MockInternalIdModel()
        model1.internal_id = 1
        model2 = _TestInternalIdModel._MockInternalIdModel()
        model2.internal_id = 2
        self.assertNotEqual(model1, model2)

    def test_can_set_internal_id_with_named_parameter(self):
        internal_id = 12334
        model = _TestInternalIdModel._MockInternalIdModel(internal_id=internal_id)
        self.assertEquals(model.internal_id, internal_id)


class _TestAccessionNumberModel(unittest.TestCase):
    """
    Tests for `AccessionNumberModel`.
    """
    class _MockAccessionNumberModel(AccessionNumberModel):
        pass

    def test_not_equal_if_different_accession_number(self):
        model1 = _TestAccessionNumberModel._MockAccessionNumberModel()
        model1.accession_number = "abc1"
        model2 = _TestAccessionNumberModel._MockAccessionNumberModel()
        model2.accession_number = "def2"
        self.assertNotEqual(model1, model2)

    def test_can_set_accession_number_with_named_parameter(self):
        accession_number = "test_123"
        model = _TestAccessionNumberModel._MockAccessionNumberModel(accession_number=accession_number)
        self.assertEquals(model.accession_number, accession_number)


class _TestIsCurrentModel(unittest.TestCase):
    """
    Tests for `IsCurrentModel`.
    """
    class _MockIsCurrentModel(IsCurrentModel):
        pass

    def test_not_equal_if_different_is_current(self):
        model1 = _TestIsCurrentModel._MockIsCurrentModel()
        model1.is_current = False
        model2 = _TestIsCurrentModel._MockIsCurrentModel()
        model2.is_current = True
        self.assertNotEqual(model1, model2)

    def test_can_set_is_current_with_named_parameter(self):
        is_current = False
        model = _TestIsCurrentModel._MockIsCurrentModel(is_current=is_current)
        self.assertEquals(model.is_current, is_current)


class TestSample(unittest.TestCase):
    """
    Tests for `Sample`.
    """
    def test_can_set_sample_specific_properties_with_named_parameters(self):
        sample = Sample(organism=ORGANISM, common_name=COMMON_NAME, taxon_id=TAXON_ID, gender=GENDER,
                        ethnicity=ETHNICITY, cohort=COHORT, country_of_origin=COUNTRY_OF_ORIGIN,
                        geographical_region=GEOGRAPHICAL_REGION)
        self.assertEquals(sample.organism, ORGANISM)
        self.assertEquals(sample.common_name, COMMON_NAME)
        self.assertEquals(sample.taxon_id, TAXON_ID)
        self.assertEquals(sample.ethnicity, ETHNICITY)
        self.assertEquals(sample.cohort, COHORT)
        self.assertEquals(sample.country_of_origin, COUNTRY_OF_ORIGIN)
        self.assertEquals(sample.geographical_region, GEOGRAPHICAL_REGION)


class TestStudy(unittest.TestCase):
    """
    Tests for `Study`.
    """
    def test_can_set_study_specific_properties_with_named_parameters(self):
        study = Study(study_type=STUDY_TYPE, description=DESCRIPTION, study_title=STUDY_TITLE,
                      study_visibility=STUDY_VISIBILITY, faculty_sponsor=FACULTY_SPONSOR)
        self.assertEquals(study.study_type, STUDY_TYPE)
        self.assertEquals(study.description, DESCRIPTION)
        self.assertEquals(study.study_title, STUDY_TITLE)
        self.assertEquals(study.study_visibility, STUDY_VISIBILITY)
        self.assertEquals(study.faculty_sponsor, FACULTY_SPONSOR)


class TestLibrary(unittest.TestCase):
    """
    Tests for `Library`.
    """
    def test_can_set_library_specific_properties_with_named_parameters(self):
        library = Library(library_type=LIBRARY_TYPE)
        self.assertEquals(library.library_type, LIBRARY_TYPE)


class TestMultiplexedLibrary(unittest.TestCase):
    """
    Tests for `MultiplexedLibrary`.
    """
    pass


class TestWell(unittest.TestCase):
    """
    Tests for `Well`.
    """
    pass


if __name__ == '__main__':
    unittest.main()
