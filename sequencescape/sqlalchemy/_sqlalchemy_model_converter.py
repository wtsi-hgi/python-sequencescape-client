from sequencescape.sqlalchemy._sqlalchemy_model import *
from sequencescape.model import *


_SQLALCHEMY_TO_POPO_CONVERSIONS = {
    SQLAlchemySample: Sample,
    SQLAlchemyStudy: Study,
    SQLAlchemyLibrary: Library,
    SQLAlchemyWell: Well,
    SQLAlchemyMultiplexedLibrary: MultiplexedLibrary,
    SQLAlchemyStudySamplesLink: Study
}


def get_equivalent_popo_model_type(sqlalchemy_type: type) -> type:
    """
    TODO
    :param sqlalchemy_type:
    :return:
    """
    if sqlalchemy_type not in _SQLALCHEMY_TO_POPO_CONVERSIONS:
        return None

    return _SQLALCHEMY_TO_POPO_CONVERSIONS[sqlalchemy_type]


def get_equivalent_sqlalchemy_model_type(popo_type: type) -> type:
    """
    TODO
    :param popo_type:
    :return:
    """
    if popo_type not in _SQLALCHEMY_TO_POPO_CONVERSIONS.values():
        return None

    return [x for x in _SQLALCHEMY_TO_POPO_CONVERSIONS.items() if x == popo_type]


def convert_to_popo_model(sqlalchemy_model: SQLAlchemyModel) -> Model:
    """
    TODO
    :param sqlalchemy_model:
    :return:
    """
    type = sqlalchemy_model.__class__
    convert_to_type = get_equivalent_popo_model_type(type)

    if convert_to_type is None:
        raise ValueError("SQLAlchemy models of type %s have not been setup for automatic conversion" % type)

    converted = convert_to_type()
    assert issubclass(converted, Model)

    for property_name, value in vars(sqlalchemy_model).items():
        converted.__dict__[property_name] = value

    return converted
