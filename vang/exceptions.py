class VangError(Exception):
    def __init__(self, msg=None, key=None):
        self.msg = msg or {}
        self.key = key


class InitError(Exception):
    pass
