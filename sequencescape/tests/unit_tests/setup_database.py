import tempfile
import sqlite3
from sequencescape.sqlalchemy._sqlalchemy_database_connector import *
from sequencescape.sqlalchemy._sqlalchemy_mapper import *
from sequencescape.tests.unit_tests.mocks import *

def create_database():
    # Note: Not using an in-memory database because the ORM closes connections to it, hence destroying it, which is
    #       not desired in some situations.
    file_handle, database_file_path = tempfile.mkstemp()
    
    dialect = "sqlite"

    connection = sqlite3.connect(database_file_path)

    cursor = connection.cursor()
    cursor.execute(
        """
            CREATE TABLE current_samples (
                name text, internal_id integer, accession_number text, organism text, common_name text,
                taxon_id text, gender text, ethnicity text, cohort text, country_of_origin text,
                geographical_region text, is_current integer
            )
        """
    )
    cursor.execute(
        """
            CREATE TABLE current_studies (
                name text, internal_id integer, accession_number text, description text, study_title text,
                study_type text, study_visibility text, faculty_sponsor text, is_current integer
            )
        """
    )
    cursor.execute(
        """
            CREATE TABLE current_library_tubes (
                name text, internal_id integer, library_type text, is_current integer
            )
        """
    )
    cursor.execute(
        """
            CREATE TABLE current_wells (
                name text, internal_id integer, is_current integer
            )
        """
    )
    cursor.execute(
        """
            CREATE TABLE current_multiplexed_library_tubes (
                name text, internal_id integer, is_current integer
            )
        """
    )
    cursor.execute(
        """
            CREATE TABLE current_study_samples (
                internal_id integer, sample_internal_id integer, study_internal_id integer, is_current integer
            )
        """
    )
    connection.commit()

    # connector = SQLAlchemyDatabaseConnector("%s:///%s" % (dialect, database_file_path))
    #
    # sample_mapper = SQLAlchemySampleMapper(connector)
    # sample_mapper.add(create_mock_sample())
    #
    # study_mapper = SQLAlchemyStudyMapper(connector)
    # study_mapper.add(create_mock_study())
    #
    # library_mapper = SQLAlchemyLibraryMapper(connector)
    # library_mapper.add(create_mock_library())
    #
    # well_mapper = SQLAlchemyWellMapper(connector)
    # well_mapper.add(create_mock_well())
    #
    # multiplexed_library_mapper = SQLAlchemyMultiplexedLibraryMapper(connector)
    # multiplexed_library_mapper.add(create_mock_multiplexed_library())


    # cursor.execute("SELECT * FROM current_samples")
    # print(cursor.fetchone())


    connection.close()


    return database_file_path, dialect

