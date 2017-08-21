import os
import datetime
import json
from documents import documents as load_all_documents

# Should set this to 16. Otherwise use
# Number of Jobs appears to be a problem.
# This is deactivated at the moment
# import multiprocessing
# N_JOBS = multiprocessing.cpu_count() * 2

BATCH_SIZE = 128
ITERATIONS = 50
MAX_DF = .75
MIN_DF = .25
N_TOP_WORDS = 10
N_TOPICS = 20
LEARNING_OFFSET = 3.

# doc_topic_prior : float, optional (default=None)
# Prior of document topic distribution theta. If the value is None,
 # defaults to 1 / n_components. In the literature, this is called alpha.

DOC_TOPIC_PRIOR = .50

# topic_word_prior : float, optional (default=None)
# Prior of topic word distribution beta. If the value is None,
# defaults to 1 / n_components. In the literature, this is called eta.

TOPIC_WORD_PRIOR = .50

DOCUMENT_REFERENCE = 'all.txt'

run = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
TOPIC_DIRECTORY = 'topics-' + run

CONFIG_FIELDS = 'BATCH_SIZE ITERATIONS MAX_DF MIN_DF N_TOP_WORDS N_TOPICS LEARNING_OFFSET DOCUMENT_REFERENCE DOC_TOPIC_PRIOR TOPIC_WORD_PRIOR'.split()
CONFIG_FILE = 'config.json'

config = {
    key:value
    for key, value in globals().items()
    if key in CONFIG_FIELDS
}

os.makedirs(TOPIC_DIRECTORY)

config_path = os.path.join(TOPIC_DIRECTORY, CONFIG_FILE)
with open(config_path, 'w') as cfg:
    cfg.write(json.dumps(config, indent=2))


def prepare_document(document):
    return document.replace('\n', ' ')


def documents():
    with open(DOCUMENT_REFERENCE, 'r') as file:
        for line in file:
            yield line.strip()


def load(path):
    if not path:
        return
    try:
        with open(path) as file:
            content = file.read()
        return prepare_document(content)
    except:
        return ''


def print_top_words(model, feature_names, n_top_words):
    for index, topic in enumerate(model.components_):
        f = [(feature_names[i], round(float(topic[i]), 2)) for i in topic.argsort()[:-n_top_words - 1:-1]]

        print('Topic %s, Weight: %s' % (index, round(float(sum(v for n,v in f)), 3) ))
        print(f)


def ensure_string(term):
    if type(term) is bytes:
        return bytes.decode(term, 'utf-8')
    try:
        return str(term)
    except:
        return '<unreadable term>'



def write_topics(model, feature_names):
    print('Writing topics')
    for topic_index, topic in enumerate(model.components_):
        filename = '%s.txt' % topic_index
        path = os.path.join(TOPIC_DIRECTORY, filename)
        with open(path, 'w') as f:
            for index in topic.argsort():
                term = feature_names[index]
                term = ensure_string(term)
                score = topic[index]
                line = '%s;%s\n' % (term, score)
                try:
                    f.write(line)
                except:
                    pass


if __name__ == '__main__':
    import datetime
    start = datetime.datetime.now()
    init_ts = datetime.datetime.now()

    documents = load_all_documents(DOCUMENT_REFERENCE)

    print(len(documents), 'documents loaded')
    end = datetime.datetime.now()
    print('Elapsed', end - start)

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    print('Vectorization')
    start = datetime.datetime.now()
    tfidf_vectorizer = TfidfVectorizer(min_df=MIN_DF,
                                       max_df=MAX_DF,
                                       lowercase=True,
                                       strip_accents='unicode',
                                       stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    end = datetime.datetime.now()
    print('Elapsed', end - start)

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