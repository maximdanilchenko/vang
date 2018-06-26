from abc import ABC, abstractmethod


class FieldABC(ABC):
    def __init__(self):
        self.parent = None

    @abstractmethod
    def validate(self, key, data):
        """ Validate key from data """
