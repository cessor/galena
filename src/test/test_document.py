from kazookid import Substitute
from nose.tools import *


def test_allowed_characters():
    # Arrange
    from galena.document import AllowedCharacters
    input_string = '_!@#(*)_)_(++}#"%#\;''#+word word'

    # Systen under Test
    allowed_characters = AllowedCharacters(input_string)

    # Act
    string = ''.join(allowed_characters)

    # Assert
    assert_equal(string, 'word word')


def test_string():
    # Arrange
    from galena.document import String
    characters = ['a', 'b', 'c']
    # System under Test
    string = String(characters)

    # Act
    str_ = str(string)

    # Assert
    assert_equal(str_, 'abc')


def test_stopwords_folder():
    # Arrange
    from galena.stopwords import StopwordsFolder
    directory = Substitute()

    file_a = Substitute()
    file_a.content.returns('A\nB')

    file_b = Substitute()
    file_b.content.returns('C\nD')

    directory.yields([file_a, file_b])

    # System under Test
    folder = StopwordsFolder(directory)

    # Act
    words = list(folder)

    # Assert
    assert_equal(words, ['a', 'b', 'c', 'd'])


def test_lexicon():
    # Arrange
    from galena.stopwords import Lexicon

    # System under Test
    lexicon = Lexicon(['a', 'b'], ['c', 'd'])

    # Act, Assert
    for c in 'abcd':
        assert_true(c in lexicon)


def test_stopwords():
    # Arrange
    from galena.stopwords import Stopwords

    # System under Test
    stopwords = Stopwords(['word'])

    # Act
    words = stopwords.remove_from(['term', 'word'])

    # Assert
    words = list(words)
    assert_equal(words, ['term'])



def test_document():
    from galena.document import Document

    words = []

    # Arrange
    stopwords = Substitute()
    stopwords.remove_from.returns(['c', 'd'])

    # System under Test
    document = Document(words, without=stopwords)

    # Act
    str_ = document.content()

    # Assert
    assert_equal(str_, 'c d')


def test_integration():

    from galena.document import Document, Text, String, AllowedCharacters
    from galena.stopwords import Stopwords, Lexicon
    from galena.remove import NewLines, Dashes, Fragments, Gaps

    # Arrange
    string = "The - quick brown     fox JUMPS over the lazy dd   dog."

    # System under Test
    text = Text(
        String(AllowedCharacters(string)),
        without=(NewLines(), Dashes(), Fragments(), Gaps())
    )

    stopwords = Stopwords(
        Lexicon(['dog', 'fox', 'quick', 'brown'])
    )

    document = Document(text, without=stopwords)

    # Act
    result = document.content()

    # Assert
    assert_equal(result, 'the jumps over the lazy')