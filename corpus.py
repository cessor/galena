import os

# def ensure_string(term):
#     if type(term) is bytes:
#         return bytes.decode(term, 'utf-8')
#     try:
#         return str(term)
#     except:
#         return '<unreadable term>'


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
        self._content = None

    def content(self):
        if not self._content:
            with open(self._path, 'r') as file:
                self._content = file.read()
        return self._content

    def __str__(self):
        return self._path

    def __repr__(self):
        return '<File: %s>' % self.__str__()


class Prepared(object):

    def __init__(self, file, preparations):
        self._file = file
        self._preparations = preparations
        self._content = None

    def _prepare(self, file):
        content = file.content()
        for prepare in self._preparations:
            content = prepare(content)
        return content

    def content(self):
        if not self._content:
            self._content = self._prepare(self._file)
        return self._content


class Lexicon(object):
    def __init__(self, words):
        self._words = words

    def __iter__(self):
        for words in self._words:
            yield from words


class Words(object):
    def __init__(self, file):
        self._file = file
        self._words = None

    def __iter__(self):
        if not self._words:
            self._words = [word.lower().strip()
                           for word in self._file.content().split('\n')]
        return self._words.__iter__()


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
        if not self._documents:
            self._documents = [Prepared(file, self._preparations)
                               for file in self._files]
        return self._documents
