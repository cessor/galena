from nose.tools import *
from kazookid import Substitute

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


def test_remove_character_fragments():
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
        stopwords.remove,
    ]

    #prepared = Prepared(File('corpus_oo/00003969.txt'), preparations)
    #print(sorted(prepared.content().split()))#

    c = Corpus(Directory('corpus_oo'), preparations)
    d = c.documents()[10]
    print(d._file._path)
    print(' '.join(d.content().split()[:100]))

