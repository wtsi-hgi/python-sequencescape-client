from sequencescape.database_connector import DatabaseConnector
from sequencescape.common import wrappers


class Mapper:
    """
    Object through which connections to the database can be made
    """
    _database_connector = None

    def __init__(self, database_connector: DatabaseConnector) -> None:
        """
        Default constructor.
        :param database_connector: the object through which database connections can be made
        """
        self._database_connector = database_connector

    def get_database_connector(self) -> DatabaseConnector:
        """
        Gets the object through which database connections can be made.
        :return: the database connector
        """
        return self._database_connector

    @wrappers.check_args_not_none
    def __get_many_by_name(self, query_model, names):
        """ This function queries the database for all the entity names given as parameter as a batch.
            Parameters
            ----------
            engine
                Database engine to run the queries on
            query_model
                A model class - predefined in serapis.seqscape.models e.g. Sample, Study
            keys
                A list of keys (name) to run the query for
            Returns
            -------
            obj_list
                Returns a list of objects of type query_model found to match the keys given as parameter.
        """
        if not names:
            return []
        session = self.get_database_connector().create_session()
        result = session.query(query_model). \
            filter(query_model.name.in_(names)). \
            filter(query_model.is_current == 1).all()
        session.close()
        return result

    @wrappers.check_args_not_none
    def __get_many_by_internal_id(self, query_model, internal_ids):
        """ This function queries the database for all the entity internal ids given as parameter as a batch.
            Parameters
            ----------
            engine
                Database engine to run the queries on
            query_model
                A model class - predefined in serapis.seqscape.models e.g. Sample, Study
            keys
                A list of internal_ids to run the query for
            Returns
            -------
            obj_list
                Returns a list of objects of type query_model found to match the internal_ids given as parameter.
        """
        if not internal_ids:
            return []
        session = self.get_database_connector().create_session()
        result = session.query(query_model). \
            filter(query_model.internal_id.in_(internal_ids)). \
            filter(query_model.is_current == 1).all()
        session.close()
        return result

    @wrappers.check_args_not_none
    def __get_many_by_accession_number(self, query_model, accession_numbers):
        """ This function queries the database for all the entity accession_number given as parameter as a batch.
            Parameters
            ----------
            engine
                Database engine to run the queries on
            query_model
                A model class - predefined in serapis.seqscape.models e.g. Sample, Study
            keys
                A list of accession_number to run the query for
            Returns
            -------
            obj_list
                Returns a list of objects of type query_model found to match the accession_number given as parameter.
        """
        if not accession_numbers:
            return []
        session = self.get_database_connector().create_session()
        result = session.query(query_model). \
            filter(query_model.accession_number.in_(accession_numbers)). \
            filter(query_model.is_current == 1).all()
        session.close()
        return result

    # This function is a "generic" version of the above - a string is used as an argument instead of in the method name
    # @wrappers.check_args_not_none
    # def __query_all_as_batch(self, query_model, ids, id_type):
    #     """ This function is for internal use - it queries seqscape for all the entities or type query_model
    #         and returns a list of results.
    #         Parameters
    #         ----------
    #         name_list
    #             The list of names for the entities you want to query about
    #         accession_number_list
    #             The list of accession numbers for all the entities you want to query about
    #         internal_id_list
    #             The list of internal_ids for all the entities you want to query about
    #         Returns
    #         -------
    #         obj_list
    #             A list of objects returned by the query of type models.*
    #     """
    #     if not ids:
    #         return []
    #     if id_type == 'name':
    #         return self.__get_many_by_name(query_model, ids)
    #     elif id_type == 'accession_number':
    #         return self.__get_many_by_accession_number(query_model, ids)
    #     elif id_type == 'internal_id':
    #         return self.__get_many_by_internal_id(query_model, ids)
    #     else:
    #         raise ValueError("The id_type parameter can only be one of the following: internal_id, accession_number, name.")

    def __get_one(self, query_model, name=None, accession_number=None, internal_id=None):
        """
        This function queries on the entity of type query_model, by one (and only one) of the identifiers:
        name, accession_number, internal_id and returns the results found in Seqscape corresponding to
        that identifier. Since it is expecting one result per identifier, it throws a ValueError if there
        are multiple rows in the DB corresponding to that identifier.
        Note: only one identifier should be provided
        Parameters
        ----------
        query_model : class
            The type of model to be queried on and returned. Can be: models.Sample or models.Study or models.Library
        name : str
            The name of the entity to query on
        accession_number : str
            The accession number of the entity to query on
        Returns
        -------
        result : query_model type
            The entity found in the database to have the identifier given as parameter
        Raises
        ------
        ValueError - if there are more rows corresponding to the identifier provided as param
        """
        if name:
            result = self.__get_many_by_name(query_model, [name])
        elif accession_number:
            result = self.__get_many_by_accession_number(query_model, [accession_number])
        elif internal_id:
            result = self.__get_many_by_internal_id(query_model, [internal_id])
        else:
            #raise ValueError("No identifier provided to query on.")
            return []
        if len(result) > 1:
            err = "This query has more than one row associated in SEQSCAPE"+str([s.name for s in result])
            raise ValueError(err)
        return result[0]

    @wrappers.check_args_not_none
    def __get_many(self, query_model, ids_as_tuples):
        results = []
        for id_type, id_val in ids_as_tuples:
            try:
                result_matching_qu = self.__get_one(**{'query_model' : query_model,id_type: id_val})
            except ValueError:
                print("Multiple entities with the same id found in the DB")
            else:
                if result_matching_qu:
                    results.append(result_matching_qu[0])
        return results

    @wrappers.check_args_not_none
    def __query_for_study_ids_by_sample_ids(self, sample_internal_ids):
        session = self.get_database_connector().create_session()
        return session.query(StudySamplesLink). \
            filter(StudySamplesLink.sample_internal_id.in_(sample_internal_ids)). \
            filter(StudySamplesLink.is_current == 1).all()
