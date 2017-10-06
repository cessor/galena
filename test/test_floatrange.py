from nose.tools import *

from corpus import *
def test_alphas():
    '''Alphas run with inclusive bounds.'''
    from galena import FloatRange
    alphas = list(FloatRange(start=0.05, end=1.0, step=0.05))
    assert_equal(alphas[0], 0.05)
    assert_equal(alphas[-1], 1.0)