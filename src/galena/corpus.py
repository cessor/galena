import os

import random
from .filesystem import *
from .document import Document

# Todo: Stemming
# Stem document
# docs <- tm_map(docs,stemDocument)



class Limited(object):

    def __init__(self, corpus):
        self._corpus = corpus

    def documents(self):
        return self._corpus.documents()[:20]


class Corpus(object):

    def __init__(self, files, preparations):
        self._files = files
        self._preparations = preparations
        self._documents = []

    def documents(self):
        raise NotImplementedError()
        return [Document(file, self._preparations)
                for file in self._files]


class Percent(object):

    def __init__(self, percent):
        self._percent = percent

    def __mul__(self, other):
        return other * self._percent / 100


class Shuffled(object):

    def __init__(self, corpus):
        self._corpus = corpus

    def documents(self):
        documents = self._corpus.documents()
        random.shuffle(documents)
        return documents


class Fixed(object):
    def __init__(self, corpus):
        self._corpus = corpus
        self._documents = None

    def documents(self):
        if not self._documents:
            self._documents = self._corpus.documents()
        return self._documents


class Holdout(object):

    def __init__(self, corpus, percent):
        self._corpus = corpus
        self._percent = percent

    def _corpus_size(self):
        return len(self._corpus.documents())

    def _holdout_size(self):
        return int(self._percent * self._corpus_size())

    def _keep(self):
        return self._corpus_size() - self._holdout_size()

    def documents(self):
        return self._corpus.documents()[:self._keep()]

    def holdout(self):
        return self._corpus.documents()[self._keep():]
