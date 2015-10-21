from sequencescape.sqlalchemy._sqlalchemy_model import *
from sequencescape.model import *

_COMPATIBLE_AUTOMATIC_CONVERSIONS = {
    SampleSQLAlchemyModel: Sample,
    StudySQLAlchemyModel: Study,
    LibrarySQLAlchemyModel: Library,
    WellSQLAlchemyModel: Well,
    MultiplexedLibrarySQLAlchemyModel: MultiplexedLibrary,
    StudySamplesLinkSQLAlchemyModel: Study
}


def get_compatible_model_type(sqlalchemy_model: SQLAlchemyModel) -> type:
    """
    TODO
    :param sqlalchemy_model:
    :return:
    """
    cls = sqlalchemy_model.__class__

    if cls not in _COMPATIBLE_AUTOMATIC_CONVERSIONS:
        return None

    return _COMPATIBLE_AUTOMATIC_CONVERSIONS[cls]


def convert_to_popo_model(sqlalchemy_model: SQLAlchemyModel) -> Model:
    """
    TODO
    :param sqlalchemy_model:
    :return:
    """
    cls = sqlalchemy_model.__class__
    convert_to_cls = get_compatible_model_type(sqlalchemy_model)

    if convert_to_cls is None:
        raise ValueError("SQLAlchemy models of type %s have not been setup for automatic conversion" % cls)

    convert_to = convert_to_cls()

    for property_name, value in vars(sqlalchemy_model).items():
        convert_to.__dict__[property_name] = value

    return convert_to
