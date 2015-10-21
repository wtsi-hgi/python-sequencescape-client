from sequencescape._mapper import *
from sequencescape._model import Sample


class SampleMapper(Mapper):
    @wrappers.one_argument_only
    def query_sample(self, name=None, accession_number=None, internal_id=None):
        """ This function queries seqscape for a sample, given by either name or accession number or internal id.
            Returns
            -------
            sample_list
                A list of samples found to match the query criteria - not very likely to contain
                more than 1 result, but may happen for old data
            Raises
            ------
            ValueError
                If all 3 parameters are None at the same time => nothing to query about
            ValueError
                If there are more than 1 samples matching a query on one of the ids.
        """
        return self.__get_one(Sample, name, accession_number, internal_id)

    @wrappers.check_args_not_none
    def query_all_samples_individually(self, ids_as_tuples):
        """
            Parameters
            ----------
            ids_as_tuples : list
                A list of tuples looking like: [('accession_number', 'EGA123'), ('internal_id', 12)]
            Returns
            -------
            samples : list
                A list of samples as extracted from the DB, where a sample is of type models.Sample
        """
        return self.__get_many(Sample, ids_as_tuples)

    @wrappers.check_args_not_none
    def query_all_samples_as_batch(self, ids, id_type):
        """
            Parameters
            ----------
            ids : list
                A list of sample ids (probably strings, possibly also ints if it's about internal_ids)
            id_type : str
                The type of the identifier i.e. what do the sample_ids represent
            Returns
            -------
            A list of samples, where a library is a seqscape model
        """
        return self.__get_many_by_given_id(Sample, ids, id_type)