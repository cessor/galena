from nose.tools import *
from kazookid import Substitute

from galena.corpus import *


def test_shuffle():
    '''Corpus: Shuffle returns an unordered list of documents'''
    corpus = Substitute()
    corpus.documents.returns(list(range(100)))

    # System under Test
    shuffled = Shuffled(corpus)

    # Act
    documents = shuffled.documents()

    # This test is very optimistic.
    # Theoretically, "Shuffled" may not shuffle anything
    # And this might lead to a broken test in 0,01% of all cases.
    assert_not_equal(documents, list(range(100)))


def test_fixed():
    '''Corpus: Fixed caches shuffled data'''
    # This is done so that the data is shuffled only once
    corpus = Substitute()
    corpus.documents.returns(list(range(100)))
    corpus = Shuffled(corpus)

    # System under Test
    corpus = Fixed(corpus)

    # Act
    a = corpus.documents()
    b = corpus.documents()

    # Assert
    assert_not_equal(a, list(range(100)))
    assert_equal(a, b)


def test_fixed_holdout():
    '''Corpus: Fixed Holdout of Shuffled Documents Integration Test'''
    corpus = Substitute()
    corpus.documents.returns([1, 2, 3, 4])
    holdout = Holdout(Fixed(Shuffled(corpus)), Percent(25))
    assert_equal(holdout.documents(), holdout.documents())
    assert_equal(holdout.holdout(), holdout.holdout())


def test_holdout():
    '''Corpus: Holdout splits the data into documents and holdout'''
    corpus = Substitute()
    corpus.documents.returns([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    holdout = Holdout(corpus, Percent(10))

    assert_equal(holdout.documents(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
    assert_equal(holdout.holdout(), [9])


def test_percent():
    '''Corpus: Percent calculates percentages'''
    assert_equal(Percent(100) * 50, 50)
    assert_equal(Percent(10) * 50, 5)
    assert_equal(Percent(25) * 1, 0.25)


def test_corpus():
    '''Corpus: The corpus returns cleaned documents'''
    from galena.stopwords import Stopwords, Lexicon
    from galena.remove import NewLines, Dashes, Fragments, Gaps

    # Arrange
    string = "The - quick brown     fox JUMPS over the lazy dd   dog."
    file = Substitute()
    file.content.returns(string)

    waste = (NewLines(), Dashes(), Fragments(), Gaps())
    stopwords = Stopwords(Lexicon(['the', 'lazy', 'quick', 'brown']))

    # Systems under Test
    corpus = Corpus([], waste, stopwords)

    # Act
    result = corpus._document(file).content()

    # Assert
    assert_equal(result, 'fox jumps over dog')
