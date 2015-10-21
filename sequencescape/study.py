from sequencescape._mapper import *
from sequencescape._sqlalchemy_model import Study


class StudyMapper(Mapper):
    @wrappers.one_argument_only
    def query_study(self, name=None, accession_number=None, internal_id=None):
        """ This function queries seqscape for a studies, given by either name or accession number or internal id.
            Returns
            -------
            study_list
                A list of studies found to match the query criteria - not very likely to contain
                more than 1 result, but may happen for old data
            Raises
            ------
            ValueError
                If all 3 parameters are None at the same time => nothing to query about
            ValueError
                If there are more than 1 samples matching a query on one of the ids.
        """
        return self.__get_one(Study, name, accession_number, internal_id)

    @wrappers.check_args_not_none
    def query_all_studies_individually(self, ids_as_tuples):
        """
        Parameters
        ----------
        ids_as_tuples : list
            A list of tuples looking like: [('accession_number', 'EGA123'), ('internal_id', 12)]
        Returns
        -------
        samples : list
            A list of studies as extracted from the DB, where a sample is of type models.Study
        Raises
        ------
        ValueError: if there are more than 1 study matching a query on one of the ids.
        """
        return self.__get_many(Study, ids_as_tuples)

    @wrappers.check_args_not_none
    def query_all_studies_as_batch(self, ids, id_type):
        """
            Parameters
            ----------
            ids : list
                A list of study ids - values (probably strings)
            id_type : str
                The type of the identifier i.e. what do the library_ids represent
            Returns
            -------
            A list of libraries, where a library is a seqscape model
        """
        return self.__get_many_by_given_id(Study, ids, id_type)

    @wrappers.check_args_not_none
    def query_all_studies_associated_with_samples(self, sample_internal_ids):
        """
        This function fetches from seqeuencescape all the studies that the samples given as parameter belong to.
        Parameters
        ----------
        sample_internal_ids : list
            A list of sample internal_id values, for which you wish to find out the study/studies
        Returns
        -------
        studies : list
            A list of models.Study found for the samples given as parameter by sample_internal_ids
        """
        studies_samples = query_for_study_ids_by_sample_ids(sample_internal_ids)
        if studies_samples:
            study_ids = [study_sample.study_internal_id for study_sample in studies_samples]
            return query_all_studies_as_batch(study_ids, 'internal_id')
        return []