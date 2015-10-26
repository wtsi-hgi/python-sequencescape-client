import tempfile
import sqlite3


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
    connection.close()


    return database_file_path, dialect

