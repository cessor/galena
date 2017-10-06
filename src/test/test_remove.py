from nose.tools import *
from kazookid import Substitute
from galena.remove import *


def test_remove_multiple_spaces():
    text = 'a  b c  d e  f'
    result = Gaps().remove_from(text)
    assert_equal(result, 'a b c d e f')


def test_remove_character_fragments():
    text = ' Reno NV pap W F Koyama vol pp and K Iga Frequency chirping'
    result = Fragments().remove_from(text)
    assert_equal(
        result, ' Reno   pap     Koyama vol   and   Iga Frequency chirping')

    text = 'membership models j k v mardia abstract'
    result = Fragments().remove_from(text)
    assert_equal(
        result, 'membership models       mardia abstract')
