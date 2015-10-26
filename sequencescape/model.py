from abc import ABCMeta


class Model(metaclass=ABCMeta):
    """
    Superclass that all POPOs (Plain Old Python Objects) must implement.
    """
    pass


class Named(metaclass=ABCMeta):
    name = None


class InternalID(metaclass=ABCMeta):
    internal_id = None


class AccessionNumber(metaclass=ABCMeta):
    accession_number = None


class IsCurrent(metaclass=ABCMeta):
    is_current = None


class Sample(Model, Named, InternalID, AccessionNumber, IsCurrent):
    """
    TODO
    """
    organism = None
    common_name = None
    taxon_id = None
    gender = None
    ethnicity = None
    cohort = None
    country_of_origin = None
    geographical_region = None

    #TODO: Does a POPO model need these (how does Python do equality?)
    def __eq__(self, other):
        return self.name == other.name and \
               self.accession_number == other.accession_number and \
               self.internal_id == other.internal_id

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "{ internal_id=%s, name=%s, accession_number=%s }" % (self.internal_id, self.name, self.accession_number)

    def __repr__(self):
        return "{ internal_id=%s, name=%s, accession_number=%s }" % (self.internal_id, self.name, self.accession_number)


class Study(Model, Named, InternalID, AccessionNumber, IsCurrent):
    """
    TODO
    """
    study_type = None
    description = None
    study_title = None
    study_visibility = None
    faculty_sponsor = None

    def __eq__(self, other):
        return self.name == other.name and \
               self.accession_number == other.accession_number and \
               self.internal_id == other.internal_id

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "{ internal_id=%s, name=%s, accession_number=%s }" % (self.internal_id, self.name, self.accession_number)

    def __repr__(self):
        return "{ internal_id=%s, name=%s, accession_number=%s }" % (self.internal_id, self.name, self.accession_number)


class Library(Model, Named, InternalID, IsCurrent):
    """
    TODO
    """
    library_type = None


class Well(Model, Named, InternalID, IsCurrent):
    """
    TODO
    """
    pass


class MultiplexedLibrary(Model, Named, InternalID, IsCurrent):
    """
    TODO
    """
    pass


class StudySamplesLink(Model, InternalID, IsCurrent):
    """
    TODO
    """
    sample_internal_id = None
    study_internal_id = None

