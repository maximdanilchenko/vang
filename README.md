# Vang

![Status: developing](https://img.shields.io/badge/status-developing-red.svg) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Vang (from "vanguard") - is validating library. 
Its API is very like ```marshmallow```'s, 
because ```marshmallow``` is awesome and many are familiar with it, 
so it will be easier to start with ```vang``` for newcomers. 
Its aims are __simplicity__ and __speed__.

### To be short its main features are:
- Simplicity;
- Speed;
- Annotation types support.

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
  - [x] ```Dict``` class;
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
- [x] Flexible errors configuration:
  - [x] Dynamic error building with all exceptions;
  - [x] Validation level param - validate while first exception raises, while all and so on.
- [x] Annotation types support:
  - [x] Mapping annotations to fields classes.
- [ ] Improves:
  - [ ] Benchmarks and speed up schema and fields ```validate``` 
method with cython if needed and where needed.
- [ ] 95% more tests coverage.

### Usage example:
```python
import typing
import pprint

from vang import fields, Schema, validators, VangError, Levels, after_validation


class Address(Schema):
    street = fields.String()
    house = fields.Integer()
    city = fields.String(default="New York")


class Car(Schema):
    name = fields.String()
    new = fields.Boolean(required=False)
    number = fields.Integer(default=None, validators=[validators.Range(1, 999)])


class User(Schema):
    # you can use type hints:
    name: str
    mapping: typing.Dict[str, int]
    age: fields.Integer(allow_none=True)
    # or as usual:
    address = fields.Nested(Address())
    cars = fields.List(Car())
    nums = fields.List(fields.Integer())
    brother = fields.Nested("self", required=False, only=("name", "age"))
    friends = fields.List("self", only=("name",))

    @after_validation(order=0)
    def add_info(self, data):
        data['info'] = 'info'
        return data

    @after_validation(order=1)
    def double_info(self, data):
        data['info'] = data['info'] * 2
        return data


user_schema = User(level=Levels.HIGH)

try:
    validated = user_schema.validate(
        {
            "name": "Bob",
            "age": None,
            "nums": [1, 2, 3, 4, 5],
            "mapping": {"some": 345},
            "cars": [
                {"name": "Ford Focus", "new": True, "number": 432},
                {"name": "Toyota Supra", "number": 432},
            ],
            "address": {"street": "High", "house": 8},
            "brother": {"name": "Alex", "age": 6},
            "friends": [{"name": "Max"}, {"name": "David"}],
        }
    )
except VangError as ve:
    pprint.pprint(ve.msg)
else:
    pprint.pprint(validated)
```
Output:
```python
{'address': {'city': 'New York', 'house': 8, 'street': 'High'},
 'age': None,
 'brother': {'age': 6, 'name': 'Alex'},
 'cars': [{'name': 'Ford Focus', 'new': True, 'number': 432},
          {'name': 'Toyota Supra', 'number': 432}],
 'friends': [{'name': 'Max'}, {'name': 'David'}],
 'info': 'infoinfo',
 'mapping': {'some': 345},
 'name': 'Bob',
 'nums': [1, 2, 3, 4, 5]}
```

