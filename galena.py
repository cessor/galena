import os
import datetime
import json
import datetime
import itertools

import numpy as np

from moment import Moment
from multiprocessing import Pool
from corpus import *
from prepare import *
from lda import *

#from documents import documents as load_all_documents

# Should set this to 16. Otherwise use
# Number of Jobs appears to be a problem.
# This is deactivated at the moment
# import multiprocessing
# N_JOBS = multiprocessing.cpu_count() * 2



def save(i, params, perplexity, start, end):
    params['perplexity'] = perplexity
    params['start'] = str(start)
    params['end'] = str(end)

    filename = 'run-%s.txt' % i
    with open(filename, 'w') as f:
        f.write(json.dumps(params, indent=2))


class FloatRange(object):
    def __init__(self, start, end, step, precision=4):
        self._start = start
        self._end = end
        self._step = step
        self._precision = precision

    def __iter__(self):
        # Exclude 0.0, because it produces errors
        value = self._start
        while value < self._end + self._step:
            yield round(value, self._precision)
            value += self._step


def make_run(run):
    i, alpha, eta, documents, holdout, n_topics = run
    start = Moment.now()

    # Improvement:
    # The Holdout --> Corpus
    # Corpus --> Documents (Iterable)
    # Corpus -> documents() returns Contents
    # Corpus -> holdout() returns Contents


    document_term_matrix = DocumentTermMatrix(
        Contents(documents),
        CountVectorizer(
            **CountVectorizerConfig(min_df=0.1, max_df=0.9).config()
        )
    )

    # Before, eta was fixed at 0.5
    #ALPHA = 0.365


    lda = LatentDirichletAllocationModel(
        document_term_matrix,
        LDAConfig(alpha=alpha, eta=eta, n_topics=N_TOPICS)
    )

    topics = lda.topics()

    # Improvement:
    # Make it so that the document term matrix is contained within
    # The LDA, so that the LDAModel cares about it.

    validation_terms = document_term_matrix.transform(
        Contents(holdout)
    )

    perplexity = topics.perplexity(validation_terms)

    end = Moment.now()
    return (i, topics.parameters(), perplexity, start, end)

if __name__ == '__main__':

    stopwords = Stopwords(
        Lexicon(

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

    holdout = Holdout(
        Fixed(Shuffled(Corpus(Directory('corpus_oo'), preparations))),
        Percent(10)
    )

    N_TOPICS = 120
    alphas = np.linspace(0.001, 0.8, num=20)
    etas = np.linspace(0.001, 0.8, num=20)

    runs = []
    for alpha in alphas:
        for eta in etas:
            runs.append((alpha, eta))

    runs = [(i, alpha, eta, holdout.documents(), holdout.holdout(), N_TOPICS)
         for i, (alpha, eta) in enumerate(runs)]

    print('Running this shit')
    with Pool(processes=16) as pool:
        for result in pool.imap_unordered(make_run, runs):
            save(*result)
    print('Done running this shit')

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

