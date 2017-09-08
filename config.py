
N_TOPICS = 120
BATCH_SIZE = 2048
ITERATIONS = 1024
MAX_DF = .95
MIN_DF = .05
N_TOP_WORDS = 10

LEARNING_OFFSET = 50.

# 0.8 & 0.8 is kind of what I want....

# doc_topic_prior : float, optional (default=None)
# Prior of document topic distribution theta. If the value is None,
# defaults to 1 / n_components. In the literature, this is called alpha.

DOC_TOPIC_PRIOR = .8

# topic_word_prior : float, optional (default=None)
# Prior of topic word distribution beta. If the value is None,
# defaults to 1 / n_components. In the literature, this is called eta.

TOPIC_WORD_PRIOR = .01




CONFIG_FIELDS = 'BATCH_SIZE ITERATIONS MAX_DF MIN_DF N_TOP_WORDS N_TOPICS LEARNING_OFFSET DOCUMENT_REFERENCE DOC_TOPIC_PRIOR TOPIC_WORD_PRIOR'.split()
CONFIG_FILE = 'config.json'

config = {
    key:value
    for key, value in globals().items()
    if key in CONFIG_FIELDS
}



config_path = os.path.join(TOPIC_DIRECTORY, CONFIG_FILE)
with open(config_path, 'w') as cfg:
    cfg.write(json.dumps(config, indent=2))

