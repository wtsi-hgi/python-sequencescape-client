from abc import ABCMeta, abstractmethod
import unittest

from sequencescape.model import Model, NamedModel, IsCurrentModel, InternalIdModel, AccessionNumberModel
from sequencescape.tests.mocks import create_mock_library, create_mock_sample, create_mock_study, create_mock_well, \
    create_mock_multiplexed_library


class _FakeModel(Model):
    pass


class _TestModel(unittest.TestCase, metaclass=ABCMeta):
    """
    Superclass for tests on `Model` classes.
    """
    def test_equal_non_nullity(self):
        self.assertNotEqual(self._create_model(), None)

    def test_equal_different_type(self):
        self.assertNotEqual(self._create_model(), _FakeModel())

    def test_equal_reflexivity(self):
        model = self._create_model()
        self.assertEqual(model, model)

    def test_equal_symmetry(self):
        model1 = self._create_model()
        model2 = self._create_model()
        self.assertEqual(model1, model2)
        self.assertEqual(model2, model1)

    def test_equal_transitivity(self):
        model1 = self._create_model()
        model2 = self._create_model()
        model3 = self._create_model()
        self.assertEqual(model1, model2)
        self.assertEqual(model2, model3)
        self.assertEqual(model1, model3)

    def test_hash_equal_if_equal(self):
        model1 = self._create_model()
        model2 = self._create_model()
        self.assertEquals(hash(model1), hash(model2))


    def test_can_get_string_representation(self):
        string_representation = str(self._create_model())
        self.assertTrue(isinstance(string_representation, str))

    @abstractmethod
    def _create_model(self):
        """
        TODO
        :return:
        """
        pass


class _TestNamed(_TestModel, metaclass=ABCMeta):
    """
    TODO
    """
    def test_not_equal_if_different_name(self):
        model1 = self._create_model()    # type: Named
        assert isinstance(model1, NamedModel)
        model1.name = "this"
        model2 = self._create_model()    # type: Named
        model2.name = "that"
        self.assertNotEqual(model1, model2)


class _TestInternalID(_TestModel, metaclass=ABCMeta):
    """
    TODO
    """
    def test_not_equal_if_different_id(self):
        model1 = self._create_model()    # type: InternalID
        assert isinstance(model1, InternalIdModel)
        model1.internal_id = 1
        model2 = self._create_model()    # type: InternalID
        model2.internal_id = 2
        self.assertNotEqual(model1, model2)


class _TestAccessionNumber(_TestModel, metaclass=ABCMeta):
    """
    TODO
    """
    def test_not_equal_if_different_accession_number(self):
        model1 = self._create_model()    # type: AccessionNumber
        assert isinstance(model1, AccessionNumberModel)
        model1.accession_number = "abc1"
        model2 = self._create_model()    # type: AccessionNumber
        model2.accession_number = "def2"
        self.assertNotEqual(model1, model2)


class _TestIsCurrent(_TestModel, metaclass=ABCMeta):
    """
    TODO
    """
    def test_not_equal_if_different_is_current(self):
        model1 = self._create_model()    # type: IsCurrent
        assert isinstance(model1, IsCurrentModel)
        model1.is_current = 0
        model2 = self._create_model()    # type: IsCurrent
        model2.is_current = 1
        self.assertNotEqual(model1, model2)


class TestSample(_TestNamed, _TestInternalID, _TestAccessionNumber, _TestIsCurrent):
    """
    TODO
    """
    def _create_model(self):
        return create_mock_sample()


class TestStudy(_TestNamed, _TestInternalID, _TestAccessionNumber, _TestIsCurrent):
    """
    TODO
    """
    def _create_model(self):
        return create_mock_study()


class TestSampleLibrary(_TestNamed, _TestInternalID, _TestIsCurrent):
    """
    TODO
    """
    def _create_model(self):
        return create_mock_library()


class TestWell(_TestNamed, _TestInternalID, _TestIsCurrent):
    """
    TODO
    """
    def _create_model(self):
        return create_mock_well()


class TestSampleModel(_TestNamed, _TestInternalID, _TestAccessionNumber, _TestIsCurrent):
    """
    TODO
    """
    def _create_model(self):
        return create_mock_sample()


class TestMultiplexedLibrary(_TestNamed, _TestInternalID, _TestIsCurrent):
    """
    TODO
    """
    def _create_model(self):
        return create_mock_multiplexed_library()


if __name__ == '__main__':
    unittest.main()
