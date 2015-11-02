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


class NamedModel(Model, metaclass=ABCMeta):
    """
    Model that has a name.
    """
    def __init__(self):
        super(NamedModel, self).__init__()
        self.name = None


class InternalIdModel(Model, metaclass=ABCMeta):
    """
    Model that has an internal ID.
    """
    def __init__(self):
        super(InternalIdModel, self).__init__()
        self.internal_id = None

    def __hash__(self) -> hash:
        return hash(self.internal_id)


class AccessionNumberModel(Model, metaclass=ABCMeta):
    """
    Model that has an accession number.
    """
    def __init__(self):
        super(AccessionNumberModel, self).__init__()
        self.accession_number = None


class IsCurrentModel(Model, metaclass=ABCMeta):
    """
    Model that has an is_current property.
    """
    def __init__(self):
        super(IsCurrentModel, self).__init__()
        self.is_current = None


class Sample(NamedModel, InternalIdModel, AccessionNumberModel, IsCurrentModel):
    """
    Model of a sample.
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


class Study(NamedModel, InternalIdModel, AccessionNumberModel, IsCurrentModel):
    """
    Model of a study.
    """
    def __init__(self):
        super(Study, self).__init__()
        self.study_type = None
        self.description = None
        self.study_title = None
        self.study_visibility = None
        self.faculty_sponsor = None


class Library(NamedModel, InternalIdModel, IsCurrentModel):
    """
    Model of a library.
    """
    def __init__(self):
        super(Library, self).__init__()
        self.library_type = None


class Well(NamedModel, InternalIdModel, IsCurrentModel):
    """
    Model of a well.
    """
    def __init__(self):
        super(Well, self).__init__()


class MultiplexedLibrary(NamedModel, InternalIdModel, IsCurrentModel):
    """
    Model of a multiplexed library.
    """
    def __init__(self):
        super(MultiplexedLibrary, self).__init__()
