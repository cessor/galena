import os
import datetime
import json
#from documents import documents as load_all_documents

# Should set this to 16. Otherwise use
# Number of Jobs appears to be a problem.
# This is deactivated at the moment
# import multiprocessing
# N_JOBS = multiprocessing.cpu_count() * 2


class LdaData(object):

    def __init__(self):
        stopwords = Stopwords(
            Lexicon(
                [Words(file) for file in Directory('stopwords')]
                + [NltkStopwords()]
            )
        )

        preparations = [
            text,
            remove_new_lines,
            remove_dashes,
            str.lower,
            remove_character_fragments,
            remove_spaces,
            stopwords.remove
        ]

        self._holdout = Holdout(
            Shuffled(Limited(Corpus(Directory('corpus_oo'), preparations))),
            Percent(10)
        )

    def training_matrix(self):
        # This returns a proper object, on which you must call
        # .matrix() when passing it to LDA
        count_vectorizer_config = CountVectorizerConfig(min_df=0.1, max_df=0.9)
        self._document_term_matrix = DocumentTermMatrix(
            Contents(self._holdout.documents()),
            CountVectorizer(**count_vectorizer_config.test())
        )
        return self._document_term_matrix

    def validation_matrix(self):
        # This returns a raw, transformed object. Do not call .matrix()
        # when passing this to perplexity
        #
        # This is not what I want. LDA manipulates the actual matrix
        # So I don't see a way how to quickly make this into an
        # Immutable thing. - JH, 09.09.2017
        return self._document_term_matrix.transform(
            Contents(self._holdout.holdout())
        )


class LdaTask(object):

    def __init__(self, document_term_matrix):
        self._document_term_matrix = document_term_matrix

    def run(self, lda_config):
        lda = LatentDirichletAllocationModel(
            self._document_term_matrix,
            lda_config
        )
        return lda.topics()


class Configurations():

    def __init__(self):
        self._n_topics = 120

    def __iter__(self):
        alphas = map(lambda v: float(v) / 100, range(0, 100, 5))
        configs = [LDAConfig(alpha=alpha, eta=0.5, n_topics=self._n_topics)
                   for alpha in alphas]
        return configs.__iter__()


if __name__ == '__main__':

    from corpus import *
    from prepare import *
    from lda import *

    lda_data = LdaData()

    config = list(Configurations())[0]
    task = LdaTask(lda_data.training_matrix())
    topics = task.run(config)

    #perplexity = topics.perplexity(lda_data.validation_matrix())

    #print(perplexity)


    # with multiprocessing.Pool(15):
    # for result in multiprocessing.imap_unordered(run_lda, Configurations()):



    # import datetime
    # start = datetime.datetime.now()
    # init_ts = datetime.datetime.now()

    # #print(l.get_params(deep=True))
    # #print(l.perplexity(m2.matrix()))

    # #get_params(deep=True)[source]
    # # --> Config Model, Topics, Perplexity, Matrix

    # print(len(documents), 'documents loaded')
    # end = datetime.datetime.now()
    # print('Elapsed', end - start)

    # tfidf_matrix = tfidf_vectorizer
    # end = datetime.datetime.now()
    # print('Elapsed', end - start)

    # # n_jobs=N_JOBS

    # lda.fit(tfidf_matrix)
    # end = datetime.datetime.now()
    # print('Elapsed', end - start)

    # print('Go')

    # feature_names = tfidf_vectorizer.get_feature_names()
    # print_top_words(lda, feature_names, N_TOP_WORDS)
    # write_topics(lda, feature_names)

    # end_ts = datetime.datetime.now()
    # print('Elapse', end_ts - init_ts)


# print('LDA')
# start = datetime.datetime.now()
# print('Start', start)


#     # start = datetime.datetime.now()
# t0 = time()
# tf = tf_vectorizer.fit_transform(data_samples)
# print("done in %0.3fs." % (time() - t0))
# print()
