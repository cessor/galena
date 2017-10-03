from nose.tools import *
from kazookid import Substitute

from lda import *
from corpus import *
from prepare import *


def test_prepare():
    # Arrange, Dependent-On Components
    file = Substitute()
    file.content.returns('aaa')

    def prepare(text):
        return text.replace('a', 'b')

    # System under Test
    prepared = Prepared(file, [prepare])

    # Act
    text = prepared.content()

    # Assert
    assert_equal(text, 'bbb')


def test_corpus():
    # Arrange, Dependent-On Components
    file = Substitute()
    file.content.returns('a\na')
    files = [file]

    def prepare(text):
        return text.replace('a', 'b')

    def remove_newlines(text):
        return text.replace('\n', ' ')

    # System under Test
    corpus = Corpus(files, [prepare, remove_newlines])

    # Act
    document = corpus.documents()[0]

    # Assert
    assert_equal(document.content(), 'b b')


def test_remove_multiple_spaces():
    text = 'a  b c  d e  f'
    result = remove_spaces(text)
    assert_equal(result, 'a b c d e f')


def test_remove_citations():
    text = 'As quoted in Hofmeister, 2003 [14]'
    result = remove_citations(text)
    assert_equal(result, 'As quoted in Hofmeister, 2003  ')


def test_remove_multiple_citations():
    text = 'As quoted in Hofmeister, 2003 [14, 21]'
    result = remove_citations(text)
    assert_equal(result, 'As quoted in Hofmeister, 2003  ')


def test_remove_bracketed_enumerations():
    text = '(a) (1) (12)'
    result = remove_brackets(text)
    assert_equal(result, '     ')


def test_replace_roman_numerals():
    text = 'I, II, III, IV, V, VI, VII, VIII, IX, X'
    result = remove_roman_numerals(text)
    assert_equal(result, ' ,  ,  ,  ,  ,  ,  ,  ,  ,  ')


def test_replace_roman_numerals_on_word_boundary():
    text = 'Isabell plays the Xylophone'
    result = remove_roman_numerals(text)
    assert_equal(result, 'Isabell plays the Xylophone')


def test_remove_character_fragments():
    text = ' Reno NV pap W F Koyama vol pp and K Iga Frequency chirping'
    result = remove_character_fragments(text)
    assert_equal(
        result, ' Reno   pap     Koyama vol   and   Iga Frequency chirping')

    text = 'membership models j k v mardia abstract'
    result = remove_character_fragments(text)
    assert_equal(
        result, 'membership models       mardia abstract')

def _test_remove_splitters():
    '''I end up with many splitters. Remove them'''
    text = ' t feW exp iwt - - - - w - dwwhere -- Eou'
    result = remove_splitters(text)
    assert_equal(result, ' t feW exp iwt   w - dwwhere   Eou')


def test_stopwords():

    file = Substitute()
    file.content.returns('a\nb')

    file2 = Substitute()
    file2.content.returns('c\nd')

    list_ = list(Lexicon([Words(file), Words(file2), ['e', 'f']]))
    assert_equal(list_, ['a', 'b', 'c', 'd', 'e', 'f'])


def _test_remove_character_fragments():
    from corpus import File, Prepared, Stopwords

    stopwords = Stopwords(
        Lexicon(
              [Words(file) for file in Directory('stopwords')]
            + [NltkStopwords()]
        )
    )

    preparations = [
        text,
        remove_new_lines,
        remove_dashes,
        str.lower,
        remove_character_fragments,
        remove_spaces,
        stopwords.remove
    ]

    corpus = Corpus(Directory('corpus_oo'), preparations)
    print(corpus.documents()[0].content())


def test_holdout():
    corpus = Substitute()
    corpus.documents.returns([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    holdout = Holdout(corpus, Percent(10))

    assert_equal(holdout.documents(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
    assert_equal(holdout.holdout(), [9])


def _test_lda():

    class Document(object):
        def __init__(self, content):
            self._content = content

        def content(self):
            return self._content

    corpus = Substitute()
    corpus.documents.returns([
        Document('aa aa aa aa tt'),
        Document('bb bb aa aa ff'),
        Document('aa aa aa cc tt'),
        Document('cc cc cc bb tt'),
        Document('aa bb aa bb tt'),
        Document('cc cc cc aa tt'),
    ])

    matrix = DocumentTermMatrix(
        corpus.documents(),
        CountVectorizer(max_df=0.90, min_df=.05)
    )

    pseudo_holdout = DocumentTermMatrix(
        corpus.documents(),
        CountVectorizer(max_df=0.90, min_df=.05)
    )

    config = LDAConfig(alpha=0.5, eta=0.1, n_topics=5)
    lda = LatentDirichletAllocationModel(
        matrix,
        config
    )

    topics = lda.topics()
    topics.perplexity(pseudo_holdout.matrix())

