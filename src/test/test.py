from nose.tools import *
from kazookid import Substitute

from galena.lda import *
from galena.corpus import *


def test_corpus():
    # Arrange, Dependent-On Components
    file = Substitute()
    file.content.returns('a\na')
    files = [file]

    def prepare(text):
        return text.replace('a', 'b')

    def remove_newlines(text):
        return text.replace('\n', ' ')

    # System under Test
    corpus = Corpus(files, [prepare, remove_newlines])

    # Act
    document = corpus.documents()[0]

    # Assert
    assert_equal(document.content(), 'b b')


def test_holdout():
    corpus = Substitute()
    corpus.documents.returns([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    holdout = Holdout(corpus, Percent(10))

    assert_equal(holdout.documents(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
    assert_equal(holdout.holdout(), [9])


def _test_lda():

    class Document(object):
        def __init__(self, content):
            self._content = content

        def content(self):
            return self._content

    corpus = Substitute()
    corpus.documents.returns([
        Document('aa aa aa aa tt'),
        Document('bb bb aa aa ff'),
        Document('aa aa aa cc tt'),
        Document('cc cc cc bb tt'),
        Document('aa bb aa bb tt'),
        Document('cc cc cc aa tt'),
    ])

    matrix = DocumentTermMatrix(
        corpus.documents(),
        CountVectorizer(max_df=0.90, min_df=.05)
    )

    pseudo_holdout = DocumentTermMatrix(
        corpus.documents(),
        CountVectorizer(max_df=0.90, min_df=.05)
    )

    config = LDAConfig(alpha=0.5, eta=0.1, n_topics=5)
    lda = LatentDirichletAllocationModel(
        matrix,
        config
    )

    topics = lda.topics()
    topics.perplexity(pseudo_holdout.matrix())

