from sequencescape._sqlalchemy_model import Library, MultiplexedLibrary
from sequencescape._mapper import Mapper
from sequencescape.common import wrappers


class LibraryMapper(Mapper):
    @wrappers.one_argument_only
    def get_library(self, name: str=None, accession_number: str=None, internal_id: str=None):
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
        return self.__get_one(Library, name, accession_number, internal_id)

    @wrappers.check_args_not_none
    def get_libraries(self, ids_as_tuples):
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
        return self.__get_many(Library, ids_as_tuples)

    @wrappers.check_args_not_none
    def get_libraries_with_property_values(self, ids, id_type):
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
        return self.__get_many_by_given_id(Library, ids, id_type)

    # TODO: Find out what this means in the domain
    @wrappers.check_args_not_none
    def query_all_multiplexed_libraries_as_batch(self, ids, id_type):
        return self.__get_many_by_given_id(MultiplexedLibrary, ids, id_type)