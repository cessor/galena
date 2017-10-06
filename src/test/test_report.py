from nose.tools import *
from kazookid import Substitute

import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def step():
    import statistics
    deltas = [b - a for a,b in pairwise(data)]
    print(statistics.mean(deltas))


def test_domain():
    import random
    data = list(range(1, 10))

        # series = Substitute()

        # series.min.returns(1)
        # series.max.returns(10)
        # series.count.returns(10)

        # domain = Domain(series)

        #
