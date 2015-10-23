from sequencescape.model import *


INTERNAL_ID = "123"
NAME = "NAME123"
ACCESSION_NUMBER = "ACCESSION_NUMBER123"
IS_CURRENT = "1"

ORGANISM = "ORGANISM123"
COMMON_NAME = "COMMON_NAME123"
TAXON_ID = "TAXON_ID123"
GENDER = "GENDER123"
ETHNICITY = "ETHNICITY123"
COHORT = "COHORT123"
COUNTRY_OF_ORIGIN = "COUNTRY_OF_ORIGIN123"
GEOGRAPHICAL_REGION = "GEOGRAPHICAL_REGION123"

STUDY_TYPE = "STUDY_TYPE123"
DESCRIPTION = "DESCRIPTION123"
STUDY_TITLE = "STUDY_TITLE123"
STUDY_VISIBILITY = "STUDY_VISIBILITY123"
FACULTY_SPONSOR = "FACULTY_SPONSOR123"

LIBRARY_TYPE = "LIBRARY_TYPE123"

SAMPLE_INTERNAl_ID = "456"
STUDY_INTERNAL_ID = "789"


def create_mock_sample() -> Sample:
    sample = Sample()
    sample.internal_id = INTERNAL_ID
    sample.name = NAME
    sample.accession_number = ACCESSION_NUMBER
    sample.organism = ORGANISM
    sample.common_name = COMMON_NAME
    sample.taxon_id = TAXON_ID
    sample.gender = GENDER
    sample.ethnicity = ETHNICITY
    sample.cohort = COHORT
    sample.country_of_origin = COUNTRY_OF_ORIGIN
    sample.geographical_region = GEOGRAPHICAL_REGION
    sample.is_current = IS_CURRENT
    return sample


def create_mock_study() -> Study:
    study = Study()
    study.internal_id = INTERNAL_ID
    study.name = NAME
    study.accession_number = ACCESSION_NUMBER
    study.study_type = STUDY_TYPE
    study.description = DESCRIPTION
    study.study_title = STUDY_TITLE
    study.study_visibility = STUDY_VISIBILITY
    study.faculty_sponsor = FACULTY_SPONSOR
    study.is_current = IS_CURRENT
    return study


def create_mock_library() -> Library:
    library = Library()
    library.internal_id = INTERNAL_ID
    library.name = NAME
    library.library_type = LIBRARY_TYPE
    library.is_current = IS_CURRENT
    return library


def create_mock_well() -> Well:
    well = Well()
    well.internal_id = INTERNAL_ID
    well.name = NAME
    well.is_current = IS_CURRENT
    return well


def create_mock_multiplexed_library() -> MultiplexedLibrary:
    multiplexed_library = MultiplexedLibrary()
    multiplexed_library.internal_id = INTERNAL_ID
    multiplexed_library.name = NAME
    multiplexed_library.is_current = IS_CURRENT
    return multiplexed_library


def create_mock_study_samples_link() -> StudySamplesLink:
    study_samples_link = StudySamplesLink()
    study_samples_link.internal_id = INTERNAL_ID
    study_samples_link.is_current = IS_CURRENT
    return study_samples_link