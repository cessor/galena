import re


class NewLines(object):

    def remove(self, text):
        return text.replace('\n', ' ').replace('\r', ' ')


class Spaces(object):
    SPACES = re.compile(r'\b +\b')

    def remove(self, text):
        return re.sub(self.SPACES, ' ', text)


class Dashes(object):

    def remove(self, text):
        return text.replace('-', ' ')


class Fragments(text):
    CHARACTER_FRAGMENTS = re.compile(r'\b([A-Z]{1,2}|[a-z]{1}|[a-z]{2})\b')

    def remove(self, text):
        return re.sub(self.CHARACTER_FRAGMENTS, ' ', text)


class Stopwords(object):

    def __init__(self, stopwords):
        self._stopwords = stopwords

    def remove(self, text):
        return ' '.join([word for word in text.words()
                         if word not in self._stopwords])