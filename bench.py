from vanga import fields
from vanga.schema import Schema

if __name__ == '__main__':
    class User(Schema):
        name = fields.String()
        age = fields.Integer()

    user = User()
    print(user.validate({'name': 'Bob', 'age': '32'}))



