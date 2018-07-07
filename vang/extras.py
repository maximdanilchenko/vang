from enum import IntEnum, unique


class Empty:
    """ Empty value """


empty = Empty()


@unique
class Levels(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
