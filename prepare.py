# encoding: utf-8
import re
import string

ALLOWED_CHARACTERS = string.ascii_letters + ' -\n' + 'äöüÄÖÜß'
SPACES = re.compile(r'\b +\b')
CITATIONS = re.compile(r'\[[\d, ]+\]')
BRACKETS = re.compile(r'\(([a-zA-Z\.]|[0-9]+)\)')
ROMAN_NUMERALS = re.compile(r'\b((I{1,3}[VX]?)|([VX]I{0,3}))\b')
CHARACTER_FRAGMENTS = re.compile(r'\b([A-Z]{1,2}|[a-z]{1}|[a-z]{2})\b')

'''
All items are replaced with spaces and multiple spaces
are later removed separately to prevent
false binding of words, e.g.

Incorret:
    'hello[1]word' --> helloworld

Correct:
    'hello[1]word' --> hello world

Correct:
    'hello[1] word' --> hello  world
'''


def remove_new_lines(text):
    return text.replace('\n', ' ').replace('\r', ' ')


def remove_citations(text):
    return re.sub(CITATIONS, ' ', text)


def remove_brackets(text):
    return re.sub(BRACKETS, ' ', text)


def remove_roman_numerals(text):
    #text = 'I, II, III, IV, V, VI, VII, VIII, IX, X'
    return re.sub(ROMAN_NUMERALS, ' ', text)

# Only the latter one's are used.
# I developed the above functions first
# and then decided that I could limit
# to only characters.


def remove_spaces(text):
    return re.sub(SPACES, ' ', text)


def remove_dashes(text):
    return text.replace('-', ' ')


def remove_character_fragments(text):
    return re.sub(CHARACTER_FRAGMENTS, ' ', text)


def text(string):
    return ''.join((c for c in string if c in ALLOWED_CHARACTERS))
