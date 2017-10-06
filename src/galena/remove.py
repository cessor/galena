import re


class NewLines(object):
    '''Removes new-line characters from a string'''
    def remove(self, string):
        return string.replace('\n', ' ').replace('\r', ' ')


class Gaps(object):
    '''Removes gaps spaces from strings'''

    SPACES = re.compile(r'\b +\b')

    def remove(self, string):
        return re.sub(self.SPACES, ' ', string)


class Dashes(object):
    '''Removes dashes from a string'''
    def remove(self, string):
        return string.replace('-', ' ')


class Fragments(object):
    '''Removes single or repeated characters from a string'''
    CHARACTER_FRAGMENTS = re.compile(r'\b([A-Z]{1,2}|[a-z]{1}|[a-z]{2})\b')

    def remove(self, string):
        return re.sub(self.CHARACTER_FRAGMENTS, ' ', string)
