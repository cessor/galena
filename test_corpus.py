from nose.tools import *
from kazookid import Substitute

from corpus import *

def test_shuffle():
    '''Shuffle Returns an Unordered List'''
    corpus = Substitute()
    corpus.documents.returns(list(range(100)))
    shuffled = Shuffled(corpus)
    assert_not_equal(shuffled.documents(), list(range(100)))


def test_holdout():
    corpus = Substitute()
    corpus.documents.returns([1, 2, 3, 4])
    holdout = Holdout(Fixed(Shuffled(corpus)), Percent(25))
    assert_equal(holdout.documents(), holdout.documents())


def test_alphas():
    '''Alphas run with inclusive bounds.'''
    from galena import AlphaSteps
    alphas = list(AlphaSteps(start=0.05, end=1.0, step=0.05))
    assert_equal(alphas[0], 0.05)
    assert_equal(alphas[-1], 1.0)
