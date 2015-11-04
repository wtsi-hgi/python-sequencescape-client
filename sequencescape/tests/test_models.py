import unittest

from sequencescape.tests.model_stub_helpers import *


class _FakeModel(Model):
    pass


class _TestModel(unittest.TestCase, metaclass=ABCMeta):
    """
    Superclass for tests on `Model` classes.
    """
    def __init__(self, model_type: type, *args, **kwargs):
        """
        Default constructor.
        :param model_type: the type of model being tested
        """
        super(_TestModel, self).__init__(*args, **kwargs)
        assert issubclass(model_type, Model)
        self.model_type = model_type

    def test_equal_non_nullity(self):
        self.assertNotEqual(self._create_mock(), None)

    def test_equal_different_type(self):
        self.assertNotEqual(self._create_mock(), _FakeModel())

    def test_equal_reflexivity(self):
        model = self._create_mock()
        self.assertEqual(model, model)

    def test_equal_symmetry(self):
        model1 = self._create_mock()
        model2 = self._create_mock()
        self.assertEqual(model1, model2)
        self.assertEqual(model2, model1)

    def test_equal_transitivity(self):
        model1 = self._create_mock()
        model2 = self._create_mock()
        model3 = self._create_mock()
        self.assertEqual(model1, model2)
        self.assertEqual(model2, model3)
        self.assertEqual(model1, model3)

    def test_hash_equal_if_equal(self):
        model1 = self._create_mock()
        model2 = self._create_mock()
        self.assertEquals(hash(model1), hash(model2))

    def test_can_get_string_representation(self):
        string_representation = str(self._create_mock())
        self.assertTrue(isinstance(string_representation, str))

    def _create_mock(self):
        """
        Creates a mock of the model that this test deals with.
        :return: mock model
        """
        return create_stub(self.model_type)


class _TestNamedModel(_TestModel, metaclass=ABCMeta):
    """
    Tests for `NamedModel`.
    """
    def test_not_equal_if_different_name(self):
        model1 = self._create_mock()    # type: NamedModel
        assert isinstance(model1, NamedModel)
        model1.name = "this"
        model2 = self._create_mock()    # type: NamedModel
        model2.name = "that"
        self.assertNotEqual(model1, model2)

    def test_can_set_name_with_named_parameter(self):
        name = "test_name"
        model = self.model_type(name=name)    # type: NamedModel
        self.assertEquals(model.name, name)


class _TestInternalIdModel(_TestModel, metaclass=ABCMeta):
    """
    Tests for `InternalIdModel`.
    """
    def test_not_equal_if_different_id(self):
        model1 = self._create_mock()    # type: InternalIdModel
        assert isinstance(model1, InternalIdModel)
        model1.internal_id = 1
        model2 = self._create_mock()    # type: InternalIdModel
        model2.internal_id = 2
        self.assertNotEqual(model1, model2)

    def test_can_set_internal_id_with_named_parameter(self):
        internal_id = 12334
        model = self.model_type(internal_id=internal_id)    # type: InternalIdModel
        self.assertEquals(model.internal_id, internal_id)


class _TestAccessionNumberModel(_TestModel, metaclass=ABCMeta):
    """
    Tests for `AccessionNumberModel`.
    """
    def test_not_equal_if_different_accession_number(self):
        model1 = self._create_mock()    # type: AccessionNumberModel
        assert isinstance(model1, AccessionNumberModel)
        model1.accession_number = "abc1"
        model2 = self._create_mock()    # type: AccessionNumberModel
        model2.accession_number = "def2"
        self.assertNotEqual(model1, model2)

    def test_can_set_accession_number_with_named_parameter(self):
        accession_number = "test_123"
        model = self.model_type(accession_number=accession_number)    # type: AccessionNumberModel
        self.assertEquals(model.accession_number, accession_number)


class _TestIsCurrentModel(_TestModel, metaclass=ABCMeta):
    """
    Tests for `IsCurrentModel`.
    """
    def test_not_equal_if_different_is_current(self):
        model1 = self._create_mock()    # type: IsCurrentModel
        assert isinstance(model1, IsCurrentModel)
        model1.is_current = False
        model2 = self._create_mock()    # type: IsCurrentModel
        model2.is_current = True
        self.assertNotEqual(model1, model2)

    def test_can_set_is_current_with_named_parameter(self):
        is_current = False
        model = self.model_type(is_current=is_current)    # type: IsCurrentModel
        self.assertEquals(model.is_current, is_current)


class TestSample(_TestNamedModel, _TestInternalIdModel, _TestAccessionNumberModel, _TestIsCurrentModel):
    """
    Tests for `Sample`.
    """
    def __init__(self, *args, **kwargs):
        super(TestSample, self).__init__(Sample, *args, **kwargs)

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


class TestStudy(_TestNamedModel, _TestInternalIdModel, _TestAccessionNumberModel, _TestIsCurrentModel):
    """
    Tests for `Study`.
    """
    def __init__(self, *args, **kwargs):
        super(TestStudy, self).__init__(Study, *args, **kwargs)

    def test_can_set_study_specific_properties_with_named_parameters(self):
        study = Study(study_type=STUDY_TYPE, description=DESCRIPTION, study_title=STUDY_TITLE,
                      study_visibility=STUDY_VISIBILITY, faculty_sponsor=FACULTY_SPONSOR)
        self.assertEquals(study.study_type, STUDY_TYPE)
        self.assertEquals(study.description, DESCRIPTION)
        self.assertEquals(study.study_title, STUDY_TITLE)
        self.assertEquals(study.study_visibility, STUDY_VISIBILITY)
        self.assertEquals(study.faculty_sponsor, FACULTY_SPONSOR)


class TestLibrary(_TestNamedModel, _TestInternalIdModel, _TestIsCurrentModel):
    """
    Tests for `Library`.
    """
    def __init__(self, *args, **kwargs):
        super(TestLibrary, self).__init__(Library, *args, **kwargs)

    def test_can_set_library_specific_properties_with_named_parameters(self):
        library = Library(library_type=LIBRARY_TYPE)
        self.assertEquals(library.library_type, LIBRARY_TYPE)


class TestMultiplexedLibrary(_TestNamedModel, _TestInternalIdModel, _TestIsCurrentModel):
    """
    Tests for `MultiplexedLibrary`.
    """
    def __init__(self, *args, **kwargs):
        super(TestMultiplexedLibrary, self).__init__(MultiplexedLibrary, *args, **kwargs)


class TestWell(_TestNamedModel, _TestInternalIdModel, _TestIsCurrentModel):
    """
    Tests for `Well`.
    """
    def __init__(self, *args, **kwargs):
        super(TestWell, self).__init__(Well, *args, **kwargs)


if __name__ == '__main__':
    unittest.main()
