from vanga.abc import FieldABC
from vanga.exceptions import VangaError
from vanga.extras import empty


SELF_NESTED = "self"


class Field(FieldABC):
    """ Base field class """

    def __init__(
        self, *, default=empty, required=True, allow_none=False, validators=(), **_
    ):
        self.default = default
        self.required = required
        self.allow_none = allow_none
        self.validators = validators
        super(Field, self).__init__()

    def _func(self, value):
        return value

    def _init(self):
        """ Staff for schema init """
        pass

    def validate(self, key, data):
        try:
            value = data[key]
            if value is None and self.allow_none:
                return None
            value = self._func(value)
            for validator in self.validators:
                validator(value)
            return value
        except (ValueError, TypeError, VangaError):
            raise VangaError(f"Incorrect format for '{key}' value")
        except KeyError:
            if self.default is empty:
                if self.required is True:
                    raise VangaError(f"Missing '{key}' value")
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
        super(Nested, self).__init__(**kwargs)

    def _init(self):
        if self._schema == SELF_NESTED:
            self._schema = self.parent.__class__(**self._kwargs)

    def _func(self, value):
        return self._schema.validate(value)


class List(Nested):
    """ List of another fields """

    def __init__(self, schema, allow_empty=True, **kwargs):
        self.allow_empty = allow_empty
        super(List, self).__init__(schema, **kwargs)

    def _func(self, value):
        result = [self._schema.validate(member) for member in value]
        if not result and not self.allow_empty:
            raise VangaError("Should not be empty")
        return result


class Raw(Field):
    """ Any object """
