import json

class Json(object):

    def __init__(self, file):
        self._file = file

    def dict(self):
        return json.loads(self._file.content())

    def __getattr__(self, name):
        return self.dict()[name]