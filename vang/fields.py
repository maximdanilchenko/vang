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


class Dict(Field):
    """ Dict field """

    def __init__(self, key_schema_or_field=None, value_schema_or_field=None, **kwargs):
        self._key_schema = key_schema_or_field or Raw()
        self._value_schema = value_schema_or_field or Raw()
        self._kwargs = kwargs
        super().__init__(**kwargs)

    def init(self):
        self._key_schema._parent = self._parent
        self._value_schema._parent = self._parent

    def _func(self, value: dict):
        return {
            self._key_schema._func(key)
            if isinstance(self._key_schema, Field)
            else self._key_schema.validate(key): self._value_schema._func(value)
            if isinstance(self._key_schema, Field)
            else self._value_schema.validate(value)
            for key, value in value.items()
        }


class Nested(Field):
    """ Another field """

    def __init__(self, schema_or_field, **kwargs):
        self._schema = schema_or_field
        self._kwargs = kwargs
        super().__init__(**kwargs)

    def init(self):
        if isinstance(self._schema, Field):
            return None
        if self._schema == SELF_NESTED:
            self._schema = self._parent.__class__(**self._kwargs)
        self._schema._parent = self._parent

    def _func(self, value: Any):
        if isinstance(self._schema, Field):
            return self._schema._func(value)
        return self._schema.validate(value)


class List(Nested):
    """ List of another fields or Schemas"""

    def __init__(self, schema_or_field, allow_empty: bool = True, **kwargs):
        self.allow_empty = allow_empty
        super().__init__(schema_or_field, **kwargs)

    def _func(self, value: Iterable[Any]):
        result = []
        errors = {}
        for idx, member in enumerate(value):
            try:
                if isinstance(self._schema, Field):
                    result.append(self._schema._func(member))
                else:
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


class Date(Field):
    """ TODO: Date field """


class Time(Field):
    """ TODO: Time field """


class DateTime(Field):
    """ TODO: DateTime field """


class Decimal(Field):
    """ TODO: Decimal field """
