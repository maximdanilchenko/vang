from vanga.abc import FieldABC


class SchemaMeta(type):

    def __new__(mcs, name, bases, attrs):
        fields = {k: v for k, v in attrs.items() if isinstance(v, FieldABC)}
        instance = super(SchemaMeta, mcs).__new__(mcs, name, bases, attrs)
        instance._fields = fields
        return instance


def validator(data, attrs):
    result = {}
    for k, v in attrs.items():
        result[k] = v.validate(k, data)
    return result


class Schema(metaclass=SchemaMeta):
    def validate(self, data):
        return validator(data, self._fields)


