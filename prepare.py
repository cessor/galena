# encoding: utf-8




class Prepare(object):

    def __init__(self, characters, without):
        self._characters = characters
        self._without = without

    def text(self):
        ''.join()



# Prepare(
#     String(Lower(AllowedCharacters(document)),
#     without=(
#         NewLines()
#         Dashes(),
#         Fragments(),
#         Spaces(),
#         Stopwords()
#     )
# ).text()
