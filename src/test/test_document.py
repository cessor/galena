

from kazookid import Substitute


from nose.tools import *

from galena.remove import *

def test_allowed_characters():
    from galena.text import AllowedCharacters
    input_string = '_!@#(*)_)_(++}#"%#\;''#+word word'

    # Systen under Test
    allowed_characters = AllowedCharacters(input_string)

    # Act
    string = ''.join(allowed_characters)

    # Assert
    assert_equal(string, 'word word')


def text_without():

    file = Substitute()
    File(r'..\corpus\documents\00006308.txt').content()

    # Lower(
    #         String(

    #         )
    #     )

    # Text(
    #     ,
    #     without=(
    #         NewLines(),
    #         Dashes(),
    #         Fragments(),
    #         Gaps(),
    #     )
    # )

def document_without():
    Document(
        text,
        without=Stopwords(
            Lexicon(
                NltkStopwords(),
                StopwordsFolder(
                    Directory('..\stopwords')
                )
            )
        )
    )