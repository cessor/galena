import os


class Filter(object):

    def __init__(self, directory, pattern):
        self._directory = directory
        self._pattern = pattern

    def __iter__(self):
        for file in self._directory:
            if file.path().endswith(self._pattern):
                yield file


class Directory(object):

    def __init__(self, path):
        self._path = path

    def __iter__(self):
        yield from (
            File(file.path) for file in os.scandir(self._path)
            if file.is_file()
        )


class DirectoryTree(object):

    def __init__(self, path):
        self._path = path

    def __iter__(self):
        for root, dirs, files in os.walk(self._path):
            for file in files:
                yield File(os.path.join(root, file))


class File(object):

    def __init__(self, path):
        self._path = path

    def path(self):
        return self._path

    def content(self):
        with open(self._path, 'r') as file:
            return file.read()

    def __str__(self):
        return self.path()

    def __repr__(self):
        return '<File: %s>' % self.__str__()
