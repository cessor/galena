import os

import random
from .filesystem import *
from .document import Document, Text, String, AllowedCharacters

# Todo: Stemming
# Stem document
# docs <- tm_map(docs,stemDocument)


class Corpus(object):
    def __init__(self, files, waste, stopwords):
        self._files = files
        self._waste = waste
        self._stopwords = stopwords

    def _document(self, file):
        string = file.content()
        return Document(
            Text(
                String(AllowedCharacters(string)),
                without=self._waste
            ),
            without=self._stopwords
        )

    def documents(self):
        return [self._document(file)
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
        documents_ = list(self._corpus.documents())
        return random.sample(documents_, len(documents_))


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
