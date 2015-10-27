from abc import ABCMeta


class Model(metaclass=ABCMeta):
    """
    Superclass that all POPOs (Plain Old Python Objects) must implement.
    """
    pass


class Named(metaclass=ABCMeta):
    def __init__(self):
        self.name = None


class InternalID(metaclass=ABCMeta):
    def __init__(self):
        self.internal_id = None


class AccessionNumber(metaclass=ABCMeta):
    def __init__(self):
        self.accession_number = None


class IsCurrent(metaclass=ABCMeta):
    def __init__(self):
        self.is_current = None


class Sample(Model, Named, InternalID, AccessionNumber, IsCurrent):
    """
    TODO
    """
    def __init__(self):
        super(Sample, self).__init__()
        self.organism = None
        self.common_name = None
        self.taxon_id = None
        self.gender = None
        self.ethnicity = None
        self.cohort = None
        self.country_of_origin = None
        self.geographical_region = None

    #TODO: Does a POPO model need these (how does Python do equality?)
    #FIXME: This is not reflective, symmetric, non-null, etc.
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
    def __init__(self):
        super(Study, self).__init__()
        self.study_type = None
        self.description = None
        self.study_title = None
        self.study_visibility = None
        self.faculty_sponsor = None

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
    def __init__(self):
        super(Library, self).__init__()
        self.library_type = None


class Well(Model, Named, InternalID, IsCurrent):
    """
    TODO
    """
    def __init__(self):
        super(Well, self).__init__()


class MultiplexedLibrary(Model, Named, InternalID, IsCurrent):
    """
    TODO
    """
    def __init__(self):
        super(MultiplexedLibrary, self).__init__()


class StudySamplesLink(Model, InternalID, IsCurrent):
    """
    TODO
    """
    def __init__(self):
        super(StudySamplesLink, self).__init__()
        self.sample_internal_id = None
        self.study_internal_id = None

