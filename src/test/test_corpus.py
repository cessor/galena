from nose.tools import *
from kazookid import Substitute

from galena.corpus import *


def test_shuffle():
    '''Shuffle Returns an Unordered List'''
    corpus = Substitute()
    corpus.documents.returns(list(range(100)))
    shuffled = Shuffled(corpus)

    # This test is very optimistic.
    # Theoretically, random may not shuffle anything
    # And this might lead to a broken test in 0,01% of all cases.
    assert_not_equal(shuffled.documents(), list(range(100)))


def test_holdout():
    corpus = Substitute()
    corpus.documents.returns([1, 2, 3, 4])
    holdout = Holdout(Fixed(Shuffled(corpus)), Percent(25))
    assert_equal(holdout.documents(), holdout.documents())

