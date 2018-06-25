from vanga.abc import FieldABC
from vanga.extras import empty


class SchemaMeta(type):

    def __new__(mcs, name, bases, attrs):
        instance = super(SchemaMeta, mcs).__new__(mcs, name, bases, attrs)
        instance._fields = {k: v
                            for k, v in attrs.items()
                            if isinstance(v, FieldABC)}
        return instance


class Schema(metaclass=SchemaMeta):

    def validate(self, data):
        result = {}
        for k, v in self._fields.items():
            value = v.validate(k, data)
            if value is not empty:
                result[k] = v.validate(k, data)
        return result
