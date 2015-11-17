from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

SQLAlchemyModel = declarative_base()

study_sample_join_table = Table("study_sample_join_table", SQLAlchemyModel.metadata,
    Column("sample_internal_id", Integer, ForeignKey("current_samples.internal_id")),
    Column("study_internal_id", Integer, ForeignKey("current_studies.internal_id"))
)

class SQLAlchemyNamedModel(SQLAlchemyModel):
    __abstract__ = True
    name = Column(String)


class SQLAlchemyInternalIdModel(SQLAlchemyModel):
    __abstract__ = True
    internal_id = Column(Integer, primary_key=True)


class SQLAlchemyAccessionNumberModel(SQLAlchemyModel):
    __abstract__ = True
    accession_number = Column(String)


class SQLAlchemyIsCurrentModel(SQLAlchemyModel):
    __abstract__ = True
    is_current = Column(Integer)


class SQLAlchemySample(SQLAlchemyNamedModel, SQLAlchemyInternalIdModel, SQLAlchemyAccessionNumberModel,
                       SQLAlchemyIsCurrentModel):
    __tablename__ = "current_samples"
    organism = Column(String)
    common_name = Column(String)
    taxon_id = Column(String)
    gender = Column(String)
    ethnicity = Column(String)
    cohort = Column(String)
    country_of_origin = Column(String)
    geographical_region = Column(String)
    # studies = relationship("SQLAlchemyStudy", secondary=study_sample_join_table, backref="samples")


class SQLAlchemyStudy(SQLAlchemyNamedModel, SQLAlchemyInternalIdModel, SQLAlchemyAccessionNumberModel,
                      SQLAlchemyIsCurrentModel):
    __tablename__ = "current_studies"
    study_type = Column(String)
    description = Column(String)
    study_title = Column(String)
    study_visibility = Column(String)
    faculty_sponsor = Column(String)
    samples = relationship("SQLAlchemySample", secondary=study_sample_join_table, backref="studies", cascade_backrefs=False)


class SQLAlchemyLibrary(SQLAlchemyNamedModel, SQLAlchemyInternalIdModel, SQLAlchemyIsCurrentModel):
    __tablename__ = "current_library_tubes"
    library_type = Column(String)


class SQLAlchemyMultiplexedLibrary(SQLAlchemyNamedModel, SQLAlchemyInternalIdModel,
                                   SQLAlchemyIsCurrentModel):
    __tablename__ = "current_multiplexed_library_tubes"


# TODO: doesn"t look like this model name fits the domain very well (Wells?)
class SQLAlchemyWell(SQLAlchemyNamedModel, SQLAlchemyInternalIdModel, SQLAlchemyIsCurrentModel):
    __tablename__ = "current_wells"

