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

### Current developing progress for MVP version:
- [x] Schemas:
  - [x] Base class for schema building;
  - [x] ```validate``` method;
  - [x] ```exclude```/```only``` params.
- [ ] Fields classes:
  - [x] Base ```Field``` class with ```validate``` method;
  - [x] ```Integer``` class;
  - [x] ```Float``` class;
  - [ ] ```Decimal``` class;
  - [x] ```String``` class;
  - [x] ```Boolean``` class;
  - [ ] ```Datetime```/```Date```/```Time``` classes;
  - [x] ```List``` class;
  - [x] ```"self"``` param for ```List``` class;
  - [x] ```Nested``` class;
  - [x] ```"self"``` param for ```Nested``` class;
  - [x] ```Raw``` class.
- [ ] Fields params:
  - [x] ```default``` param;
  - [x] ```required``` param;
  - [x] ```allow_none``` param;
  - [ ] ```error_msg``` param;
  - [ ] ```validators``` param;
  - [ ] ```before_validation```/```after_validation``` params.
- [ ] Decorators:
  - [ ] ```before_validation``` decorator;
  - [ ] ```after_validation``` decorator.
- [ ] Standard validation functions:
  - [ ] ```Range``` function;
  - [ ] ```Length``` function;
  - [ ] ```OneOf``` function;
  - [ ] ```NoneOf``` function;
  - [ ] ```Equal``` function;
  - [ ] ```Regexp``` function.
- [ ] Flexible errors configuration:
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
import pprint

from vanga import fields, Schema


class Address(Schema):
    street = fields.String()
    house = fields.Integer()
    city = fields.String(default="New York")


class Car(Schema):
    name = fields.String()
    new = fields.Boolean(required=False)
    number = fields.Integer(default=None)


class User(Schema):
    name = fields.String()
    age = fields.Integer(allow_none=True)
    address = fields.Nested(Address())
    cars = fields.List(Car())
    brother = fields.Nested("self", required=False, only=("name", "age"))
    friends = fields.List("self", only=("name",))


user_schema = User()
validated = user_schema.validate(
    {
        "name": "Bob",
        "age": None,
        "cars": [
            {"name": "Ford Focus", "new": True},
            {"name": "Toyota Supra", "number": 432},
        ],
        "address": {"street": "High", "house": 43},
        "brother": {"name": "Alex", "age": 24},
        "friends": [{"name": "Max"}, {"name": "David"}],
    }
)
pprint.pprint(validated)
"""Output:
{'address': {'city': 'New York', 'house': 43, 'street': 'High'},
 'age': None,
 'brother': {'age': 24, 'name': 'Alex'},
 'cars': [{'name': 'Ford Focus', 'new': True, 'number': None},
          {'name': 'Toyota Supra', 'number': 432}],
 'friends': [{'name': 'Max'}, {'name': 'David'}],
 'name': 'Bob'}
"""
```
