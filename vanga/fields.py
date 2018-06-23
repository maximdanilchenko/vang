from abc import abstractmethod

from vanga.abc import FieldABC
from vanga.exceptions import VangaError


class Field(FieldABC):
    def __init__(self):
        """ TODO: Implement arguments like "required", "allow_none" etc """
        pass

    def _func(self, value):
        return value

    def validate(self, key, data):
        try:
            return self._func(data[key])
        except ValueError:
            raise VangaError(f'incorrect format for {key} value')
        except KeyError:
            raise VangaError(f'missing "{key}" value')


class Integer(Field):
    _func = int


class String(Field):
    _func = str


class Boolean(Field):
    _func = bool


class Nested(Field):
    def __init__(self, schema):
        self._schema = schema
        super(Nested, self).__init__()

    def validate(self, key, data):
        try:
            return self._schema.validate(data[key])
        except VangaError:
            raise VangaError(f'incorrect format for {key} value')
        except KeyError:
            raise VangaError(f'missing "{key}" value')
