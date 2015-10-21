# TODO: Make abstract
class Model:
    pass


class Sample(Model):
    internal_id = None
    name = None
    accession_number = None
    organism = None
    common_name = None
    taxon_id = None
    gender = None
    ethnicity = None
    cohort = None
    country_of_origin = None
    geographical_region = None
    is_current = None

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


class Study(Model):
    internal_id = None
    name = None
    accession_number = None
    study_type = None
    description = None
    study_title = None
    study_visibility = None
    faculty_sponsor = None
    is_current = None

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


class Library():
    internal_id = None
    name = None
    library_type = None
    is_current = None


# TODO: doesn't look like this model name fits the domain very well (Wells?)
class Well(Model):
    internal_id = None
    name = None
    is_current = None


class MultiplexedLibrary(Model):
    internal_id = None
    name = None
    is_current = None


class StudySamplesLink():
    internal_id = None
    sample_internal_id = None
    study_internal_id = None
    is_current = None

