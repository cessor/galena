from text import *
from remove import *
from corpus import File


class Document(object):

    def __init__(self, text, without):
        self._text = text
        self._stopwords = without

    def _clean(self):
        return self._stopwords.remove(self._text)

    def __str__(self):
        return ' '.join(self._clean())


from stopwords import *

doc = Document(
    Text(
        Lower(
            String.concatenate(
                AllowedCharacters(
                    File('corpus_oo/00006308.txt').content()
                )
            )
        ),
        without=(
            NewLines(),
            Dashes(),
            Fragments(),
            Gaps(),
        )
    ),
    without=Stopwords(
        Lexicon(
            NltkStopwords(),
            StopwordsFolder(
                Directory('stopwords')
            )
        )
    )
)

print(doc)



#Text is String without Waste
#Document is Text without Stopwords
