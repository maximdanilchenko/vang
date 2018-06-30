from typing import Iterable

from vanga.abc import FieldABC
from vanga.extras import empty


class SchemaMeta(type):
    def __new__(mcs, name, bases, attrs):
        instance = super(SchemaMeta, mcs).__new__(mcs, name, bases, attrs)
        instance._fields = {k: v for k, v in attrs.items() if isinstance(v, FieldABC)}

        return instance


class Schema(metaclass=SchemaMeta):
    def __init__(self, *, exclude: Iterable[str] = (), only: Iterable[str] = (), **_):
        only = set(only or self._fields.keys())
        self._fields = {
            k: prepare_field(v, self)
            for k, v in self._fields.items()
            if k not in exclude and k in only
        }

    def validate(self, data: dict):
        result = {}
        for k, v in self._fields.items():
            value = v.validate(k, data)
            if value is not empty:
                result[k] = v.validate(k, data)
        return result


def prepare_field(child: FieldABC, parent: Schema):
    child.parent = parent
    child.init()
    return child
