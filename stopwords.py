from corpus import *
from text import *
import itertools

class Stopwords(object):

    def __init__(self, stopwords):
        self._stopwords = stopwords

    def remove(self, words):
        for word in words:
            if word not in self._stopwords:
                yield word


class Lexicon(object):
    def __init__(self, *iterables):
        self._iterables = list(itertools.chain(*iterables))

    def __contains__(self, item):
        return item in self._iterables



class NltkStopwords(object):

    def __iter__(self):
        from nltk.corpus import stopwords
        return stopwords.words('english').__iter__()


class StopwordsFolder(object):
    def __init__(self, directory):
        self._directory = directory

    def __iter__(self):
        for file in self._directory:
            for line in Lines(file.content()):
                for word in Words(line):
                    if word:
                        yield word.strip().lower()

