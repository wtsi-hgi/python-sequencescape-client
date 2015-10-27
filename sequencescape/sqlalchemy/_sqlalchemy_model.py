from abc import ABCMeta

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


SQLAlchemyModel = declarative_base()


class SQLAlchemyNamed():
    __metaclass__ = ABCMeta
    name = Column(String)


class SQLAlchemyInternalID():
    __metaclass__ = ABCMeta
    internal_id = Column(Integer, primary_key=True)


class SQLAlchemyAccessionNumber():
    __metaclass__ = ABCMeta
    accession_number = Column(String)


class SQLAlchemyIsCurrent():
    __metaclass__ = ABCMeta
    is_current = Column(Integer)


class SQLAlchemySample(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyAccessionNumber, SQLAlchemyIsCurrent):
    __tablename__ = 'current_samples'

    organism = Column(String)
    common_name = Column(String)
    taxon_id = Column(String)
    gender = Column(String)
    ethnicity = Column(String)
    cohort = Column(String)
    country_of_origin = Column(String)
    geographical_region = Column(String)

    def __eq__(self, other):
        return self.name == other.name and \
               self.accession_number == other.accession_number and \
               str(self.internal_id) == str(other.internal_id)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "{ internal_id=%s, name=%s, accession_number=%s }" % (self.internal_id, self.name, self.accession_number)

    def __repr__(self):
        return "{ internal_id=%s, name=%s, accession_number=%s }" % (self.internal_id, self.name, self.accession_number)


class SQLAlchemyStudy(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyAccessionNumber, SQLAlchemyIsCurrent):
    __tablename__ = 'current_studies'

    study_type = Column(String)
    description = Column(String)
    study_title = Column(String)
    study_visibility = Column(String)
    faculty_sponsor = Column(String)

    def __eq__(self, other):
        return self.name == other.name and \
               self.accession_number == other.accession_number and \
               str(self.internal_id) == str(other.internal_id)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "{ internal_id=%s, name=%s, accession_number=%s }" % (self.internal_id, self.name, self.accession_number)

    def __repr__(self):
        return "{ internal_id=%s, name=%s, accession_number=%s }" % (self.internal_id, self.name, self.accession_number)


class SQLAlchemyLibrary(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyIsCurrent):
    __tablename__ = 'current_library_tubes'

    library_type = Column(String)

    def __eq__(self, other):
        return self.name == other.name and \
               str(self.internal_id) == str(other.internal_id)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "{ internal_id=%s, name=%s }" % (self.internal_id, self.name)

    def __repr__(self):
        return "{ internal_id=%s, name=%s }" % (self.internal_id, self.name)


# TODO: doesn't look like this model name fits the domain very well (Wells?)
class SQLAlchemyWell(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyIsCurrent):
    __tablename__ = 'current_wells'

    def __eq__(self, other):
        return str(self.internal_id) == str(other.internal_id)

    def __hash__(self):
        return hash(self.internal_id)

    def __str__(self):
        return "{ internal_id=%s }" % self.internal_id

    def __repr__(self):
        return self.__str__()


class SQLAlchemyMultiplexedLibrary(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyIsCurrent):
    __tablename__ = 'current_multiplexed_library_tubes'

    def __eq__(self, other):
        return self.name == other.name and \
               str(self.internal_id) == str(other.internal_id)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "{ internal_id=%s, name=%s }" % (self.internal_id, self.name)

    def __repr__(self):
        return "{ internal_id=%s, name=%s }" % (self.internal_id, self.name)


class SQLAlchemyStudySamplesLink(SQLAlchemyModel, SQLAlchemyInternalID, SQLAlchemyIsCurrent):
    __tablename__ = 'current_study_samples'

    sample_internal_id = Column(Integer)
    study_internal_id = Column(Integer)

    def __eq__(self, other):
        return self.sample_internal_id == other.sample_internal_id and \
               str(self.internal_id) == str(other.internal_id)

    def __hash__(self):
        return hash(self.sample_internal_id) + hash(self.study_internal_id)

    def __str__(self):
        return "{ sample_internal_id=%s, study_internal_id=%s }" % (self.sample_internal_id, self.study_internal_id)

    def __repr__(self):
        return self.__str__()
