from nose.tools import *
from kazookid import Substitute

from galena.lda import *
from galena.corpus import *


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

