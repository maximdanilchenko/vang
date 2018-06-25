from vanga.abc import FieldABC
from vanga.exceptions import VangaError
from vanga.extras import empty


class Field(FieldABC):
    """ Base field class """
    def __init__(self, *,
                 default=empty,
                 required=True,
                 allow_none=False):
        self.default = default
        self.required = required
        self.allow_none = allow_none

    def _func(self, value):
        return value

    def validate(self, key, data):
        try:
            value = data[key]
            if value is None and self.allow_none:
                return None
            return self._func(value)
        except (ValueError, TypeError, VangaError):
            raise VangaError(f'Incorrect format for {key} value')
        except KeyError:
            if self.default is empty:
                if self.required is True:
                    raise VangaError(f'Missing "{key}" value')
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
        super(Nested, self).__init__(**kwargs)

    def _func(self, value):
        return self._schema.validate(value)


class List(Field):
    """ List of fields """
    def __init__(self, schema, allow_empty=True, **kwargs):
        self._schema = schema
        self.allow_empty = allow_empty
        super(List, self).__init__(**kwargs)

    def _func(self, value):
        result = [self._schema.validate(member)
                  for member in value]
        if not result and not self.allow_empty:
            raise VangaError(f'Should not be empty')
        return result


class Raw(Field):
    """ Any object """
