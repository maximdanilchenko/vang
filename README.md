# vanga | _developing_

```python
from vanga import fields
from vanga.schema import Schema

class Address(Schema):
    street = fields.String()
    house = fields.Integer()

class User(Schema):
    name = fields.String()
    age = fields.Integer()
    address = fields.Nested(Address())

user_schema = User()
validated = user_schema.validate({
    'name': 'Bob',
    'age': '32',
    'address': {'street': 'High',
                'house': 43}
})
```
