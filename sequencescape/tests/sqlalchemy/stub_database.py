import tempfile
import sqlite3


def create_stub_database():
    """
    Creates a stub database with a number of tables found in a Sequencescape database.

    An in-memory database is not used because sqlite in-memory databases are destroyed upon close.
    :return: stub database
    """
    file_handle, database_location = tempfile.mkstemp()
    dialect = "sqlite"
    connection = sqlite3.connect(database_location)

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

    return database_location, dialect

