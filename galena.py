import os
import datetime
import json
import datetime
#from documents import documents as load_all_documents

# Should set this to 16. Otherwise use
# Number of Jobs appears to be a problem.
# This is deactivated at the moment
# import multiprocessing
# N_JOBS = multiprocessing.cpu_count() * 2



def save(i, topics, perplexity, start, end):
    params = topics.parameters()
    params['perplexity'] = perplexity
    params['start'] = str(start)
    params['end'] = str(end)

    filename = 'run-%s.txt' % i
    with open(filename, 'w') as f:
        f.write(json.dumps(params, indent=2))


class AlphaSteps(object):
    def __init__(self, start, end, step, precision=2):
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


if __name__ == '__main__':

    from corpus import *
    from prepare import *
    from lda import *

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

    holdout = Holdout(
        Fixed(Shuffled(Corpus(Directory('corpus_oo'), preparations))),
        Percent(10)
    )

    count_vectorizer_config = CountVectorizerConfig(min_df=0.1, max_df=0.9)
    document_term_matrix = DocumentTermMatrix(
        Contents(holdout.documents()),
        CountVectorizer(**count_vectorizer_config.config())
    )

    N_TOPICS = 120
    alphas = AlphaSteps(0.05, 1.0, 0.05)
    for i, alpha in enumerate(alphas):
        start = Moment.now()

        # Before, eta was fixed at 0.5
        eta = 1 / N_TOPICS
        config = LDAConfig(alpha=alpha, eta=eta, n_topics=N_TOPICS)

        lda = LatentDirichletAllocationModel(
            document_term_matrix,
            config
        )

        topics = lda.topics()

        validation_terms = document_term_matrix.transform(
            Contents(holdout.holdout())
        )

        perplexity = topics.perplexity(validation_terms)

        end = Moment.now()
        save(i, topics, perplexity, start, end)



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

