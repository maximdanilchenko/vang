import re

from vanga.exceptions import VangaError


class Range:
    """ Is >= min and <= max """

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def __call__(self, value):
        if self.min is not None and value < self.min:
            raise VangaError(f"Should be >= {self.min}")
        if self.max is not None and value > self.max:
            raise VangaError(f"Should be <= {self.max}")


class Length:
    """ Length is >= min and <= max """

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def __call__(self, value):
        if self.min is not None and len(value) < self.min:
            raise VangaError(f"Length should be >= {self.min}")
        if self.max is not None and len(value) > self.max:
            raise VangaError(f"Length should be <= {self.max}")


class OneOf:
    """ Is one of values """

    def __init__(self, values=()):
        self.values = values

    def __call__(self, value):
        if value not in self.values:
            raise VangaError(f"Length should be one of {self.values}")


class NoneOf:
    """ Is none of values """

    def __init__(self, values=()):
        self.values = values

    def __call__(self, value):
        if value in self.values:
            raise VangaError(f"Length should not be one of {self.values}")


class Equal:
    """ Is equal to value """

    def __init__(self, value):
        self.value = value

    def __call__(self, value):
        if value != self.value:
            raise VangaError(f"Should be equal to {self.value}")


class Regexp:
    """ Is match to regex """

    def __init__(self, regexp):
        self.regexp = re.compile(regexp)

    def __call__(self, value):
        if self.regexp.match(value) is None:
            raise VangaError(f"Should match to '{self.regexp}' regexp")
