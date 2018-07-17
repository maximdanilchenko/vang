from abc import ABC, abstractmethod


class FieldABC(ABC):
    def __init__(self):
        self._parent = None

    @abstractmethod
    def validate(self, key: str, data: dict):
        """ Validate key from data """

    @abstractmethod
    def init(self):
        pass
