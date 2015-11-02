from abc import ABCMeta


class Model(metaclass=ABCMeta):
    """
    Superclass that all POPOs (Plain Old Python Objects) must implement.
    """
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for property, value in vars(self).items():
            if other.__dict__[property] != self.__dict__[property]:
                return False
        return True

    def __str__(self) -> str:
        string_builder = []
        for property, value in vars(self).items():
            string_builder.append("%s: %s" % (property, value))
        return "{ %s }" % ', '.join(string_builder)


class Named(Model, metaclass=ABCMeta):
    """
    TODO
    """
    def __init__(self):
        super(Named, self).__init__()
        self.name = None


class InternalID(Model, metaclass=ABCMeta):
    """
    TODO
    """
    def __init__(self):
        super(InternalID, self).__init__()
        self.internal_id = None

    def __hash__(self) -> hash:
        return hash(self.internal_id)


class AccessionNumber(Model, metaclass=ABCMeta):
    """
    TODO
    """
    def __init__(self):
        super(AccessionNumber, self).__init__()
        self.accession_number = None


class IsCurrent(Model, metaclass=ABCMeta):
    """
    TODO
    """
    def __init__(self):
        super(IsCurrent, self).__init__()
        self.is_current = None


class Sample(Named, InternalID, AccessionNumber, IsCurrent):
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


class Study(Named, InternalID, AccessionNumber, IsCurrent):
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


class Library(Named, InternalID, IsCurrent):
    """
    TODO
    """
    def __init__(self):
        super(Library, self).__init__()
        self.library_type = None


class Well(Named, InternalID, IsCurrent):
    """
    TODO
    """
    def __init__(self):
        super(Well, self).__init__()


class MultiplexedLibrary(Named, InternalID, IsCurrent):
    """
    TODO
    """
    def __init__(self):
        super(MultiplexedLibrary, self).__init__()


# FIXME: Required?
class StudySamplesLink(InternalID, IsCurrent):
    """
    TODO
    """
    def __init__(self):
        super(StudySamplesLink, self).__init__()
        self.sample_internal_id = None
        self.study_internal_id = None
