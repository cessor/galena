# encoding: utf-8
import string


class Text(object):
    '''Removes waste from a string'''

    def __init__(self, string, without):
        self._string = string
        self._without = without

    def _clean(self):
        string = str(self._string)
        for waste in self._without:
            string = waste.remove(string)
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
    '''Represents a string that can be cleaned'''

    def __init__(self, string):
        self._string = string

    def __str__(self):
        return str(self._string)

    @classmethod
    def concatenate(cls, characters):
        return String(''.join(characters))

    def remove(self, waste):
        return String(waste.remove(self._string))

    def __iter__(self):
        yield from self._string


class AllowedCharacters(object):
    '''Filters characters from a string'''
    ALLOWED_CHARACTERS = string.ascii_letters + ' -\n' + 'äöüÄÖÜß'

    def __init__(self, string):
        self._string = string

    def __iter__(self):
        for c in self._string:
            if c in self.ALLOWED_CHARACTERS:
                yield c


class Lower(String):
    pass
    # '''Returns lower case characters'''

    def __str__(self):
        return str(self._string).lower()

    def __iter__(self):
        for c in self._string:
            yield c.lower()



class Stripped(String):
    '''Returns lower case characters'''

    def __str__(self):
        return str(self._string.strip())