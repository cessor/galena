from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

print('Vectorization')
start = datetime.datetime.now()
tfidf_vectorizer = TfidfVectorizer(min_df=MIN_DF,
                                   max_df=MAX_DF,
                                   ngram_range=(1,2),
                                   norm='l1',
                                   use_idf=True,
                                   smooth_idf=True,
                                   lowercase=True,
                                   strip_accents='unicode',
                                   stop_words='english')

print('LDA')
start = datetime.datetime.now()
print('Start', start)
lda = LatentDirichletAllocation(
    batch_size=BATCH_SIZE,
    doc_topic_prior=DOC_TOPIC_PRIOR,
    learning_method='online',
    learning_offset=LEARNING_OFFSET,
    max_iter=ITERATIONS,
    n_components=N_TOPICS,
    topic_word_prior=TOPIC_WORD_PRIOR,
    verbose=1
)