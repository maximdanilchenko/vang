import typing

from vang.fields import Field, Integer, Float, String, Boolean, List, Dict, Raw
from vang.exceptions import InitError


TYPES_MAPPING = {
    int: Integer(),
    float: Float(),
    str: String(),
    bool: Boolean(),
    list: List(Raw()),
    tuple: List(Raw()),
    dict: Dict(),
}


def _type_to_field(type_):
    if isinstance(type_, Field):
        return type_
    if type_ in TYPES_MAPPING:
        return TYPES_MAPPING[type_]
    if issubclass(type_, typing.List):
        if type_.__args__:
            return List(_type_to_field(type_.__args__[0]))
        else:
            return List(Raw())
    if issubclass(type_, typing.Dict):
        if type_.__args__:
            return Dict(*(_type_to_field(i) for i in type_.__args__))
        else:
            return Dict(Raw())
    raise InitError(
        'Wrong annotation. In case of using type hints should be one of:'
        'int, float, str, bool, list, tuple, dict, typing.List or typing.Dict'
    )


def types_to_fields(types):
    return {k: _type_to_field(v) for k, v in types.items()}
