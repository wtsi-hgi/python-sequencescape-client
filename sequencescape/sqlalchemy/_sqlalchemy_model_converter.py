from typing import List

from sequencescape.sqlalchemy._sqlalchemy_model import *
from sequencescape.model import *


# TODO: Move this to model module and make public?
_SQLALCHEMY_TO_POPO_CONVERSIONS = {
    SQLAlchemySample: Sample,
    SQLAlchemyStudy: Study,
    SQLAlchemyLibrary: Library,
    SQLAlchemyWell: Well,
    SQLAlchemyMultiplexedLibrary: MultiplexedLibrary,
    SQLAlchemyStudySamplesLink: StudySamplesLink
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
    for key, value in _SQLALCHEMY_TO_POPO_CONVERSIONS.items():
        if value == popo_type:
            return key
    return None


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
    assert issubclass(converted.__class__, Model)

    for property_name, value in vars(sqlalchemy_model).items():
        converted.__dict__[property_name] = value

    return converted


# TODO: Write test
def convert_to_popo_models(sqlalchemy_models: List[SQLAlchemyModel]) -> List[Model]:
    """
    TODO
    :param sqlalchemy_models:
    :return:
    """
    return [convert_to_popo_model(x) for x in sqlalchemy_models]


def convert_to_sqlalchemy_model(model: Model) -> SQLAlchemyModel:
    """
    TODO
    :param model:
    :return:
    """
    type = model.__class__
    convert_to_type = get_equivalent_sqlalchemy_model_type(type)

    if convert_to_type is None:
        raise ValueError("Models of type %s have not been setup for automatic conversion to SQLAlchemy models" % type)

    converted = convert_to_type()
    assert issubclass(converted.__class__, SQLAlchemyModel)

    for property_name, value in vars(model).items():
        converted.__dict__[property_name] = value

    return converted


# TODO: Write test
def convert_to_sqlalchemy_models(models: List[Model]) -> List[SQLAlchemyModel]:
    """
    TODO
    :param models:
    :return:
    """
    return [convert_to_sqlalchemy_model(x) for x in models]