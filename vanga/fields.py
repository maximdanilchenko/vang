from vanga.abc import FieldABC
from vanga.exceptions import VangaError


class Integer(FieldABC):
    def __init__(self):
        super(Integer, self).__init__()

    def validate(self, key, data):
        try:
            return int(data[key])
        except ValueError:
            raise VangaError(f'incorrect format for {key} value')
        except KeyError:
            raise VangaError(f'missing "{key}" value')


class String(FieldABC):
    def __init__(self):
        super(String, self).__init__()

    def validate(self, key, data):
        try:
            return str(data[key])
        except ValueError:
            raise VangaError(f'incorrect format for {key} value')
        except KeyError:
            raise VangaError(f'missing "{key}" value')
