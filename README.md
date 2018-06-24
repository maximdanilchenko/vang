# vanga | _developing_

```python
from vanga import fields
from vanga.schema import Schema

class Address(Schema):
    street = fields.String()
    house = fields.Integer()

class Car(Schema):
    name = fields.String()

class User(Schema):
    name = fields.String()
    age = fields.Integer()
    address = fields.Nested(Address())
    cars = fields.List(Car())

user_schema = User()
validated = user_schema.validate({
    'name': 'Bob',
    'age': '32',
    'cars': [{'name': 'Ford Focus'},
             {'name': 'Toyota Supra'}],
    'address': {'street': 'High',
                'house': 43}
})
```
