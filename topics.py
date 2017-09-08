DOCUMENT_REFERENCE = 'documents.txt'
run = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
TOPIC_DIRECTORY = 'topics-' + run


os.makedirs(TOPIC_DIRECTORY)


def print_top_words(model, feature_names, n_top_words):
    for index, topic in enumerate(model.components_):
        f = [(feature_names[i], round(float(topic[i]), 2)) for i in topic.argsort()[:-n_top_words - 1:-1]]

        print('Topic %s, Weight: %s' % (index, round(float(sum(v for n,v in f)), 3) ))
        print(f)


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