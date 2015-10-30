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


class SQLAlchemyStudy(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyAccessionNumber, SQLAlchemyIsCurrent):
    __tablename__ = 'current_studies'
    study_type = Column(String)
    description = Column(String)
    study_title = Column(String)
    study_visibility = Column(String)
    faculty_sponsor = Column(String)


class SQLAlchemyLibrary(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyIsCurrent):
    __tablename__ = 'current_library_tubes'
    library_type = Column(String)


# TODO: doesn't look like this model name fits the domain very well (Wells?)
class SQLAlchemyWell(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyIsCurrent):
    __tablename__ = 'current_wells'


class SQLAlchemyMultiplexedLibrary(SQLAlchemyModel, SQLAlchemyNamed, SQLAlchemyInternalID, SQLAlchemyIsCurrent):
    __tablename__ = 'current_multiplexed_library_tubes'


class SQLAlchemyStudySamplesLink(SQLAlchemyModel, SQLAlchemyInternalID, SQLAlchemyIsCurrent):
    __tablename__ = 'current_study_samples'
    sample_internal_id = Column(Integer)
    study_internal_id = Column(Integer)

