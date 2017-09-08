import os
import random

# Todo: Stemming
# Stem document
# docs <- tm_map(docs,stemDocument)


class Directory(object):

    def __init__(self, path):
        self._path = path

    def __iter__(self):
        for root, dirs, files in os.walk(self._path):
            for file in files:
                yield File(os.path.join(root, file))


class File(object):

    def __init__(self, path):
        self._path = path

    def content(self):
        with open(self._path, 'r') as file:
            return file.read()

    def __str__(self):
        return self._path

    def __repr__(self):
        return '<File: %s>' % self.__str__()


class Prepared(object):

    def __init__(self, file, preparations):
        self._file = file
        self._preparations = preparations

    def _prepare(self, file):
        content = file.content()
        for prepare in self._preparations:
            content = prepare(content)
        return content

    def content(self):
        return self._prepare(self._file)


class Lexicon(object):

    def __init__(self, words):
        self._words = words

    def __iter__(self):
        for words in self._words:
            yield from words


class Words(object):

    def __init__(self, file):
        self._file = file

    def __iter__(self):
        return [word.lower().strip()
                for word in self._file.content().split('\n')].__iter__()


class NltkStopwords(object):

    def __iter__(self):
        from nltk.corpus import stopwords
        return stopwords.words('english').__iter__()


class Stopwords(object):

    def __init__(self, stopwords):
        self._stopwords = list(stopwords)

    def remove(self, text):
        text = text.split()
        return ' '.join([word for word in text
                         if word not in self._stopwords])


class Corpus(object):

    def __init__(self, files, preparations):
        self._files = files
        self._preparations = preparations
        self._documents = []

    def documents(self):
        return [Prepared(file, self._preparations)
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
