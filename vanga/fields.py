from vanga.abc import FieldABC
from vanga.exceptions import VangaError
from vanga.extras import empty


class Field(FieldABC):
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
    _func = int


class String(Field):
    _func = str


class Boolean(Field):
    _func = bool


class Nested(Field):
    def __init__(self, schema, **kwargs):
        self._schema = schema
        super(Nested, self).__init__(**kwargs)

    def _func(self, value):
        return self._schema.validate(value)


class List(Field):
    def __init__(self, schema, **kwargs):
        self._schema = schema
        super(List, self).__init__(**kwargs)

    def _func(self, value):
        return [self._schema.validate(member)
                for member in value]
