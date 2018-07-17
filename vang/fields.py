from typing import Any, Iterable, Callable

from vang.abc import FieldABC
from vang.exceptions import VangError
from vang.extras import empty, Levels


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
            raise VangError(f"Incorrect format", key)
        except VangError as ve:
            if ve.key:
                ve.msg = {ve.key: ve.msg}
            ve.key = key
            raise ve
        except KeyError:
            if self.default is empty:
                if self.required is True:
                    raise VangError(f"Missing key", key)
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
            self._schema = self._parent.__class__(**self._kwargs)
        self._schema._parent = self._parent

    def _func(self, value: Any):
        return self._schema.validate(value)


class List(Nested):
    """ List of another fields """

    def __init__(self, schema, allow_empty: bool = True, **kwargs):
        self.allow_empty = allow_empty
        super().__init__(schema, **kwargs)

    def _func(self, value: Iterable[Any]):
        result = []
        errors = {}
        for idx, member in enumerate(value):
            try:
                result.append(self._schema.validate(member))
            except VangError as ve:
                if self._parent.level != Levels.HIGH:
                    ve.msg = {idx: ve.msg}
                    raise ve
                errors[idx] = ve.msg
        if errors:
            raise VangError(msg=errors)
        if not result and not self.allow_empty:
            raise VangError("Should not be empty")
        return result


class Raw(Field):
    """ Any object """
