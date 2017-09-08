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
    import datetime
    start = datetime.datetime.now()
    init_ts = datetime.datetime.now()


    print(len(documents), 'documents loaded')
    end = datetime.datetime.now()
    print('Elapsed', end - start)


    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    end = datetime.datetime.now()
    print('Elapsed', end - start)


    # n_jobs=N_JOBS

    lda.fit(tfidf_matrix)
    end = datetime.datetime.now()
    print('Elapsed', end - start)

    print('Go')

    feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(lda, feature_names, N_TOP_WORDS)
    write_topics(lda, feature_names)

    end_ts = datetime.datetime.now()
    print('Elapse', end_ts - init_ts)