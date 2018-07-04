from typing import Iterable

from vang.abc import FieldABC
from vang.extras import empty
from vang.exceptions import VangError


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
        error = None
        result = {}
        for k, v in self._fields.items():
            try:
                value = v.validate(k, data)
            except VangError as ve:
                if error is None:
                    error = VangError(key=self.__class__.__name__)
                error.msg[ve.key] = ve.msg
            else:
                if error is None and value is not empty:
                    result[k] = v.validate(k, data)
        if error:
            if len(error.msg) == 1:
                raise VangError(*list(error.msg.items())[0][::-1])
            raise VangError(error.msg, error.key)
        return result


def prepare_field(child: FieldABC, parent: Schema):
    child.parent = parent
    child.init()
    return child
