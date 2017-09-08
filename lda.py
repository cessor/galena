from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


MAX_DF = .90
MIN_DF = .05

BATCH_SIZE = 2048
ITERATIONS = 512
LDA_LEARNING_METHOD = 'online'
LEARNING_OFFSET = 50.
NGRAM_RANGE = (1, 2),
STRIP_ACCENTS = 'ascii'
VERBOSE = 0


class TfidfVectorizerConfig(object):

    def __init__(self, max_df, min_df):
        self._max_df = max_df
        self._min_df = min_df

    def conifg(self):
        return dict(
            max_df=self._max_df,
            min_df=self._min_df,
            strip_accents=STRIP_ACCENTS,
            ngram_range=NGRAM_RANGE,
            norm='l1',
        )


class CountVectorizerConfig(object):

    def __init__(self, max_df, min_df):
        self._max_df = max_df
        self._min_df = min_df

    def config(self):
        return dict(
            max_df=self._max_df,
            min_df=self._min_df,
            strip_accents=STRIP_ACCENTS,
            ngram_range=NGRAM_RANGE,
        )


class LDAConfig(object):

    def __init__(self, alpha, eta, n_topics):
        self._alpha = alpha
        self._eta = eta
        self._n_topics = n_topics

    def config(self):
        return dict(
            doc_topic_prior=self._alpha,
            topic_word_prior=self._eta,
            n_components=self._n_topics,
            batch_size=BATCH_SIZE,
            learning_method=LDA_LEARNING_METHOD,
            learning_offset=LEARNING_OFFSET,
            max_iter=ITERATIONS,
            verbose=VERBOSE
        )


class DocumentTermMatrix(object):

    def __init__(self, documents, vectorizer):
        self._documents = documents
        self._vectorizer = vectorizer

    def matrix(self):
        return self._vectorizer.fit_transform(self._documents)

    def term(self, index):
        return self._vectorizer.get_feature_names()[index]


class LatentDirichletAllocationModel(object):

    def __init__(self, document_term_matrix, config):
        self._matrix = document_term_matrix
        self._config = config

    def topics(self):
        lda = LatentDirichletAllocation(**self._config.config())
        model = lda.fit_transform(self._matrix.matrix())
        return Topics(lda, model, self._matrix)


class Topics(object):

    def __init__(self, lda, model, matrix):
        self._lda = lda
        self._model = model
        self._matrix = matrix

    def parameters(self):
        return self._lda.get_params()

    def perplexity(self, matrix):
        return self._lda.preplexity(matrix)

    def __iter__(self):
        for topic in self._lda.components_:
            yield Topic(topic, self._matrix)


class Topic(object):

    def __init__(self, topic, matrix):
        self._topic = topic
        self._matrix = matrix

    def terms(self):
        for index in self._topic.argsort():
            term = self._matrix.term(index)
            score = self._topic[index]
            yield term, round(score, 2)

    def weight(self):
        return sum(score for _, score in self.terms())
