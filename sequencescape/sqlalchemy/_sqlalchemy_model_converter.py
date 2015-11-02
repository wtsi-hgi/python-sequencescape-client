from typing import List, Union

from sequencescape.model import Study, Sample, Well, MultiplexedLibrary, Model
from sequencescape.model import Library
from sequencescape.sqlalchemy._sqlalchemy_model import SQLAlchemySample, SQLAlchemyStudy, SQLAlchemyLibrary, \
    SQLAlchemyWell, SQLAlchemyMultiplexedLibrary, SQLAlchemyModel


# TODO: Move this to model module?
_SQLALCHEMY_TO_POPO_CONVERSIONS = {
    SQLAlchemySample: Sample,
    SQLAlchemyStudy: Study,
    SQLAlchemyLibrary: Library,
    SQLAlchemyWell: Well,
    SQLAlchemyMultiplexedLibrary: MultiplexedLibrary
}


def get_equivalent_popo_model_type(sqlalchemy_type: type) -> Union[type, None]:
    """
    Gets the equivalent Plain Old Python Object (POPO) type for the given SQLAlchemy model type.
    :param sqlalchemy_type: the type of SQLAlchemy model to get equivalent POPO for
    :return: the equivalent type of POPO for the given SQLAlchemy model type. `None` if no equivalent model is known
    """
    if sqlalchemy_type not in _SQLALCHEMY_TO_POPO_CONVERSIONS:
        return None

    return _SQLALCHEMY_TO_POPO_CONVERSIONS[sqlalchemy_type]


def get_equivalent_sqlalchemy_model_type(popo_type: Union[type, None]) -> Union[type, None]:
    """
    Gets the equivalent SQLAlchemy model type for the given Plain Old Python Object (POPO).
    :param popo_type: the type of POPO model to get equivalent SQLAlchemy model for
    :return: the equivalent type of SQLAlchemy model to the given POPO. `None` if no equivalent model is known
    """
    for key, value in _SQLALCHEMY_TO_POPO_CONVERSIONS.items():
        if value == popo_type:
            return key
    return None


def convert_to_popo_model(sqlalchemy_model: SQLAlchemyModel) -> Union[Model, None]:
    """
    Converts the given SQLAlchemy model into an equivalent POPO model thus removing the coupling to the underlying ORM.
    Raises exception if cannot convert.
    :param sqlalchemy_model: the SQLAlchemy model to convert
    :return: an equivalent POPO model
    """
    if sqlalchemy_model is None:
        return None

    type = sqlalchemy_model.__class__
    convert_to_type = get_equivalent_popo_model_type(type)

    if convert_to_type is None:
        raise ValueError("SQLAlchemy models of type %s have not been setup for automatic conversion" % type)

    converted = convert_to_type()
    assert issubclass(converted.__class__, Model)

    for property_name, value in vars(sqlalchemy_model).items():
        if property_name in converted.__dict__:
            converted.__dict__[property_name] = value

    return converted


# TODO: Write test
def convert_to_popo_models(sqlalchemy_models: List[SQLAlchemyModel]) -> List[Union[Model, None]]:
    """
    Converts the given SQLAlchemy models into an equivalent POPO models thus removing the coupling to the underlying
    ORM.
    :param sqlalchemy_models: the SQLAlchemy models to convert
    :return: an equivalent POPO models
    """
    return [convert_to_popo_model(x) for x in sqlalchemy_models]


def convert_to_sqlalchemy_model(model: Model) -> Union[SQLAlchemyModel, None]:
    """
    Converts the given POPO model into an equivalent SQLAlchemy model. Raises exception if cannot convert.
    :param model: the POPO model to convert
    :return: the equivalent SQLAlchemy model
    """
    if model is None:
        return None

    type = model.__class__
    convert_to_type = get_equivalent_sqlalchemy_model_type(type)    # type: type

    if convert_to_type is None:
        raise ValueError("Models of type %s have not been setup for automatic conversion to SQLAlchemy models" % type)

    converted = convert_to_type()
    assert issubclass(converted.__class__, SQLAlchemyModel)

    for property_name, value in vars(model).items():
        converted.__dict__[property_name] = value

    return converted


def convert_to_sqlalchemy_models(models: List[Model]) -> List[Union[SQLAlchemyModel, None]]:
    """
    Converts the given POPO models into equivalent SQLAlchemy models.
    :param models: the POPO models to convert
    :return: the equivalent SQLAlchemy models
    """
    return [convert_to_sqlalchemy_model(x) for x in models]