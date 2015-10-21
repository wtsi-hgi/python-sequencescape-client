import unittest
from sequencescape.sqlalchemy._sqlalchemy_model_converter import *


INTERNAL_ID = "InternalID123"
NAME = "Name123"
ACCESSION_NUMBER = "ACCESSION_NUMBER123"
ORGANISM = "ORGANISM123"
COMMON_NAME = "COMMON_NAME123"
TAXON_ID = "TAXON_ID123"
GENDER = "GENDER123"
ETHNICITY = "ETHNICITY123"
COHORT = "COHORT123"
COUNTRY_OF_ORIGIN = "COUNTRY_OF_ORIGIN123"
GEOGRAPHICAL_REGION = "GEOGRAPHICAL_REGION123"
IS_CURRENT = "IS_CURRENT123"


class TestAutoConvertToPopoModel(unittest.TestCase):
    def test_convert_sample(self):
        alchemy_model = SampleSQLAlchemyModel()
        alchemy_model.internal_id = INTERNAL_ID
        alchemy_model.name = NAME
        alchemy_model.accession_number = ACCESSION_NUMBER
        alchemy_model.organism = ORGANISM
        alchemy_model.common_name = COMMON_NAME
        alchemy_model.taxon_id = TAXON_ID
        alchemy_model.gender = GENDER
        alchemy_model.ethnicity = ETHNICITY
        alchemy_model.cohort = COHORT
        alchemy_model.country_of_origin = COUNTRY_OF_ORIGIN
        alchemy_model.geographical_region = GEOGRAPHICAL_REGION
        alchemy_model.is_current = IS_CURRENT

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




if __name__ == '__main__':
    unittest.main()
