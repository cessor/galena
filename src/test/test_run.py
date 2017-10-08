from nose.tools import *
from kazookid import Substitute

from galena.report import Json


def test_json_dict():
    file = Substitute()
    file.content.returns('{"key": "value"}')

    # System under Test
    json = Json(file)

    # Act
    dictionary = json.dict()

    # Assert
    assert_equal(dictionary.get('key'), 'value')
