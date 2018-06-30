from typing import Any, Iterable, Callable

from vanga.abc import FieldABC
from vanga.exceptions import VangaError
from vanga.extras import empty


SELF_NESTED = "self"


class Field(FieldABC):
    """ Base field class """

    def __init__(
        self,
        *,
        default: Any = empty,
        required: bool = True,
        allow_none: bool = False,
        validators: Iterable[Callable] = (),
        **_,
    ):
        self.default = default
        self.required = required
        self.allow_none = allow_none
        self.validators = validators
        super().__init__()

    def _func(self, value: Any):
        return value

    def init(self):
        """ Staff for schema init """
        pass

    def validate(self, key: str, data: dict):
        try:
            value = data[key]
            if value is None and self.allow_none:
                return None
            value = self._func(value)
            for validator in self.validators:
                validator(value)
            return value
        except (ValueError, TypeError):
            raise VangaError(f"Incorrect format", key)
        except VangaError as ve:
            ve.key = f".{key}{ve.key}" if ve.key else f".{key}"
            raise ve
        except KeyError:
            if self.default is empty:
                if self.required is True:
                    raise VangaError(f"Missing key", f".{key}")
                return empty
            return self.default


class Integer(Field):
    """ Integer field """

    _func = int


class Float(Field):
    """ Float field """

    _func = float


class String(Field):
    """ String field """

    _func = str


class Boolean(Field):
    """ Boolean field """

    _func = bool


class Nested(Field):
    """ Another field """

    def __init__(self, schema, **kwargs):
        self._schema = schema
        self._kwargs = kwargs
        super().__init__(**kwargs)

    def init(self):
        if self._schema == SELF_NESTED:
            self._schema = self.parent.__class__(**self._kwargs)

    def _func(self, value: Any):
        return self._schema.validate(value)


class List(Nested):
    """ List of another fields """

    def __init__(self, schema, allow_empty: bool=True, **kwargs):
        self.allow_empty = allow_empty
        super().__init__(schema, **kwargs)

    def _func(self, value: Iterable[Any]):
        # result = [self._schema.validate(member) for member in value]
        result = []
        for idx, member in enumerate(value):
            try:
                result.append(self._schema.validate(member))
            except VangaError as ve:
                ve.key = f"[{idx}]{ve.key}" if ve.key else f"[{idx}]"
                raise ve
        if not result and not self.allow_empty:
            raise VangaError("Should not be empty")
        return result


class Raw(Field):
    """ Any object """
