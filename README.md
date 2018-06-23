# vanga
##### developing

```python
from vanga import fields
from vanga.schema import Schema

class User(Schema):
    name = fields.String()
    age = fields.Integer()

user_schema = User()
validated = user_schema.validate({'name': 'Bob', 'age': '32'})
```
