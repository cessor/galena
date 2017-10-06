from corpus import *


def runs(path):
    return zip(*sorted((
        (run.get('doc_topic_prior'), run.get('perplexity'))
        for run
        in (
            Json(file).dict()
            for file
            in Filter(Directory(path), '.txt')
        )
    ), key=lambda v: v[0]))


def percent(value, min, max):
    return (value - min) / (max - min)


def padding(percent):
    return int(round(percent * WINDOW_WIDTH))


if __name__ == '__main__':
    WINDOW_WIDTH = 80

    import sys
    path = sys.argv[-1]

    prior, perplexity = runs(path)

    min_ = min(perplexity)
    max_ = max(perplexity)

    for d, p in zip(prior, perplexity):
        print(d, ' ', end='')
        print('*'.rjust(padding(percent(p, min_, max_))))
