import os
import datetime
import json
#from documents import documents as load_all_documents

# Should set this to 16. Otherwise use
# Number of Jobs appears to be a problem.
# This is deactivated at the moment
# import multiprocessing
# N_JOBS = multiprocessing.cpu_count() * 2



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
        Shuffled(Corpus(Directory('corpus_oo'), preparations)),
        Percent(10)
    )

    count_vectorizer_config = CountVectorizerConfig(min_df=0.1, max_df=0.9)
    training_terms = DocumentTermMatrix(
        holdout.documents(),
        CountVectorizer(**count_vectorizer_config.config())
    )

    validation_terms = DocumentTermMatrix(
        holdout.holdout(),
        CountVectorizer(**count_vectorizer_config.config())
    )

    N_TOPICS = 120
    lda_config = LDAConfig(alpha=0.1, eta=0.1, n_topics=N_TOPICS)
    lda = LatentDirichletAllocationModel(
        training_terms,
        lda_config
    )

    topics = lda.topics()
    topics.perplexity(validation_terms)

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

