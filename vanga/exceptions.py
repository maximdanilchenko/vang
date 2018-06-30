class VangaError(Exception):
    def __init__(self, msg, key=None):
        self.msg = msg
        self.key = key

    def pmsg(self):
        if self.key:
            return f"{self.msg}: {self.key[1:]}"
        else:
            return self.msg
