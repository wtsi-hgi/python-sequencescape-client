from sequencescape._models import Library, MultiplexedLibrary
from sequencescape._query import *


@wrappers.one_argument_only
def query_library(name=None, accession_number=None, internal_id=None):
    """ This function queries seqscape for a library, given by either name or accession number or internal id.
        Returns
        -------
        library_list
            A list of libraries found to match the query criteria - not very likely to contain
            more than 1 result, but may happen for old data
        Raises
        ------
        ValueError
            If all 3 parameters are None at the same time => nothing to query about
        ValueError
            If there are more than 1 samples matching a query on one of the ids.
    """
    return query_one(Library, name, accession_number, internal_id)


@wrappers.check_args_not_none
def query_all_libraries_individually(ids_as_tuples):
    """
    Parameters
    ----------
    ids_as_tuples : list
        A list of tuples looking like: [('accession_number', 'EGA123'), ('internal_id', 12)]
    Returns
    -------
    samples : list
        A list of libraries as extracted from the DB, where a sample is of type models.Library
    Raises
    ------
    ValueError: if there are more than 1 library matching a query on one of the ids.
    """
    return query_all_individually(Library, ids_as_tuples)


@wrappers.check_args_not_none
def query_all_libraries_as_batch(ids, id_type):
    """
        Parameters
        ----------
        ids : list
            A list of library ids (probably strings)
        id_type : str
            The type of the identifier i.e. what do the library_ids represent
        Returns
        -------
        A list of libraries, where a library is a seqscape model
    """
    return query_all_as_batch(Library, ids, id_type)


@wrappers.check_args_not_none
def query_all_multiplexed_libraries_as_batch(ids, id_type):
    return query_all_as_batch(MultiplexedLibrary, ids, id_type)