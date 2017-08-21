'''
import nltk
use nltk.download()
and install models/Punkt and corpus/stopwords

'''
from nltk.corpus import stopwords
from nltk import word_tokenize

import os
import datetime


def _prepare_document(document):
    return word_tokenize(document)


def _documents(path):
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            yield line


def _load(path):
    with open(os.path.normpath(path)) as file:
        content = file.read()
        return content


def documents(document_list_path):
    '''Loads documents all documents in the list into memory
    Args:
        document_list_path: A file containing one txt document path per line.
    '''
    import multiprocessing
    n_processes = multiprocessing.cpu_count() // 2 - 1
    with multiprocessing.Pool(processes=n_processes) as pool:
        tokens = pool.imap_unordered(tokenize, _documents(document_list_path))
        return list(tokens)



def tokenize(path):
    content = _load(path)
    return path, _prepare_document(content)



if __name__ == '__main__':

    start = datetime.datetime.now()

    #tokens = list(map(tokenize, _documents('documents.txt')))
    tokens = documents('documents.txt')
    print(len(tokens))

    end = datetime.datetime.now()
    print('Elapsed: ', end - start)