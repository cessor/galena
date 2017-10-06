# encoding: utf-8
import string

class Document(object):

    def __init__(self, text, without):
        self._text = text
        self._stopwords = without

    def _clean(self):
        return self._stopwords.remove_from(self._text)

    def __str__(self):
        return self.content()

    def content(self):
        return ' '.join(self._clean())


class Text(object):
    '''Removes waste from a string'''

    def __init__(self, string, without):
        self._string = string
        self._without = without

    def _clean(self):
        string = str(self._string).lower()
        for waste in self._without:
            string = waste.remove_from(string)
        return string

    def __iter__(self):
        '''Iterating a text yields its words'''
        yield from Words(self._clean())

    def __str__(self):
        return str(self._clean())


class Words(object):

    def __init__(self, string):
        self._string = string

    def __iter__(self):
        yield from self._string.split(' ')


class Lines(object):

    def __init__(self, string):
        self._string = string

    def __iter__(self):
        yield from self._string.split('\n')


class String(object):
    def __init__(self, characters):
        self._characters = characters

    def __str__(self):
        return ''.join(self._characters)


class AllowedCharacters(object):
    '''Filters characters from a string'''
    ALLOWED_CHARACTERS = string.ascii_letters + ' -\n' + 'äöüÄÖÜß'

    def __init__(self, string):
        self._string = string

    def __iter__(self):
        for c in self._string:
            if c in self.ALLOWED_CHARACTERS:
                yield c