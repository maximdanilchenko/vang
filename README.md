# Vanga

![status](https://img.shields.io/badge/status-developing-red.svg)

Vanga (from "vanguard") - is validating library. 
Its API is very like ```marshmallow```'s, 
because ```marshmallow``` is awesome and many are familiar with it, 
so it will be easier to start with ```vanga``` for newcomers. 
Its aims are __simplicity__ and __speed__.

### To be short its main features are/will be:
- Simplicity;
- Speed;
- Annotation types support;
- Integrated json loader for speed up.

### Current developing progress:
#### Schemas:
- [x] Schema base class for schema building ;
- [x] Schema ```validate``` method;

#### Fields classes:
- [x] Integer;
- [ ] Float;
- [ ] Decimal;
- [x] String;
- [x] Boolean;
- [ ] Datetime/Date/Time;
- [x] List;
- [x] Nested;
- [ ] Raw.

#### Fields params:
- [x] default param;
- [x] required param;
- [x] allow_none param;
- [ ] error_msg param;
- [ ] validators param.

#### Annotation types support:
- [ ] Mapping annotations to fields classes.

#### Improves:
- [ ] Benchmarks and speed up schema and fields ```validate``` 
method with cython if needed and where needed.

#### Json loader integrated with validator
_In progress_...

### Example:
```python
from vanga import fields, Schema


class Address(Schema):
    street = fields.String()
    house = fields.Integer()
    city = fields.String(default='New York')


class Car(Schema):
    name = fields.String()
    new = fields.Boolean(required=False)
    number = fields.Integer(default=None)


class User(Schema):
    name = fields.String()
    age = fields.Integer(allow_none=True)
    address = fields.Nested(Address())
    cars = fields.List(Car())


user_schema = User()
validated = user_schema.validate({
    'name': 'Bob',
    'age': None,
    'cars': [{'name': 'Ford Focus', 'new': True},
             {'name': 'Toyota Supra', 'number': 432}],
    'address': {'street': 'High',
                'house': 43}
})
```
