from text import *
from remove import *
from corpus import File


class Document(object):

    def __init__(self, text, without):
        self._text = text
        self._stopwords = without

    def _clean(self):
        #self._text
        #waste = self._without
        #return waste.remove([str(word) for word in self._text])
        return list(self._stopwords.remove(self._text))

    def __str__(self):
        return str(self._clean())

    def content(self):
        return self.__str__()


from stopwords import *

text = Text(
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
)

doc = Document(
    text,
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
