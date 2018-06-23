from abc import ABC, abstractmethod


class FieldABC(ABC):

    @abstractmethod
    def validate(self, key, data):
        """ Validate key from data """



