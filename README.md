# Vang

![Status: developing](https://img.shields.io/badge/status-developing-red.svg) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Vang (from "vanguard") - is validating library. 
Its API is very like ```marshmallow```'s, 
because ```marshmallow``` is awesome and many are familiar with it, 
so it will be easier to start with ```vang``` for newcomers. 
Its aims are __simplicity__ and __speed__.

### To be short its main features are/will be:
- Simplicity;
- Speed;
- Annotation types support;
- Integrated json loader for speed up.

### Current developing progress for MVP version:
- [x] Schemas:
  - [x] Base class for schema building;
  - [x] ```validate``` method;
  - [x] ```exclude```/```only``` params.
- [ ] Fields classes:
  - [x] Base ```Field``` class with ```validate``` method;
  - [x] ```Integer``` class;
  - [x] ```Float``` class;
  - [x] ```String``` class;
  - [x] ```Boolean``` class;
  - [x] ```List``` class;
  - [x] ```"self"``` param for ```List``` class;
  - [x] ```Nested``` class;
  - [x] ```"self"``` param for ```Nested``` class;
  - [x] ```Raw``` class.
  - [ ] ```Datetime```/```Date```/```Time``` classes;
  - [ ] ```Decimal``` class;
- [x] Fields params:
  - [x] ```default``` param;
  - [x] ```required``` param;
  - [x] ```allow_none``` param;
  - [x] ```validators``` param;
- [x] Decorators:
  - [x] ```before_validation``` decorator;
  - [x] ```after_validation``` decorator;
  - [x] Optional ```order``` param to execute funcs before or after validation in given order.
- [x] Standard validation functions:
  - [x] ```Range``` function;
  - [x] ```Length``` function;
  - [x] ```OneOf``` function;
  - [x] ```NoneOf``` function;
  - [x] ```Equal``` function;
  - [x] ```Regexp``` function.
- [ ] Flexible errors configuration:
  - [x] Dynamic error building with all exceptions;
  - [x] Validation level param - validate while first exception raises, while all and so on; 
  - [ ] Configuring error messages for each validate class/function;
  - [ ] Custom exceptions support.
- [ ] Annotation types support:
  - [ ] Mapping annotations to fields classes.
- [ ] Improves:
  - [ ] Benchmarks and speed up schema and fields ```validate``` 
method with cython if needed and where needed.
- [ ] 95% more tests coverage.
- [ ] Json loader integrated with validator:
  
  _In progress_...

### Usage example:
```python
from pprint import pprint

from vang import fields, Schema, validators, VangError, Levels


class Address(Schema):
    street = fields.String()
    house = fields.Integer()
    city = fields.String(default="New York")


class Car(Schema):
    name = fields.String()
    new = fields.Boolean(required=False)
    number = fields.Integer(default=None, validators=[validators.Range(1, 999)])


class User(Schema):
    name = fields.String()
    age = fields.Integer(allow_none=True)
    address = fields.Nested(Address())
    cars = fields.List(Car())
    brother = fields.Nested("self", required=False, only=("name", "age"))
    friends = fields.List("self", only=("name",))


user_schema = User(level=Levels.HIGH)
try:
    validated = user_schema.validate(
        {
            "name": "Bob",
            "age": None,
            "cars": [
                {"name": "Ford Focus", "new": True, "number": 123456},
                {"name": "Toyota Supra", "number": 4382},
            ],
            "address": {"street": "High", "house": "not num"},
            "brother": {"name": "Alex", "age": "ten"},
            "friends": [{"name": "Max"}, {"name": "David"}],
        }
    )
except VangError as ve:
    pprint(ve.msg)
```
Output:
```python
{'address': {'house': 'Incorrect format'},
 'brother': {'age': 'Incorrect format'},
 'cars': {0: {'number': 'Should be <= 999'}, 1: {'number': 'Should be <= 999'}}}
```

