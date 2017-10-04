import string


class Document(object):


class String(object):

    def __init__(self, characters):
        self._characters = characters

    def __str__(self):
        return ''.join(self._characters)


class AllowedCharacters(object):
    ALLOWED_CHARACTERS = string.ascii_letters + ' -\n' + 'äöüÄÖÜß'

    def __init__(self, text):
        self._text = text

    def __iter__(self):
        for c in self._string:
            if c in ALLOWED_CHARACTERS:
                yield c


class Lower(object):

    def __init__(self, characters):
        self._characters = characters

    def __iter__(self):
        for c in self._characters:
            yield c.lower()