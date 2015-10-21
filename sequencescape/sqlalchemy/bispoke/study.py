from sequencescape.mapper import *


class StudyMapper(Mapper):
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