from nose.tools import *
from moment import *

import datetime


def test_moment():
    '''Moment: A moment represents a point in time'''
    now = datetime.datetime(2017, 10, 3, 17, 23, 38, 921081)
    moment = Moment(now)
    assert_equal(str(moment), '2017-10-03_17-23')


def test_duration_between_moments():
    '''Moment: A duration between two moments'''
    start = datetime.datetime(2017, 10, 3, 17, 23, 41, 921081)
    end = datetime.datetime(2017, 10, 4, 19, 24, 41, 921081)

    start = Moment(start)
    end = Moment(end)

    duration = (end - start)
    assert_equal(duration, Duration(93660))


def test_duration_equals():
    '''Duration: Durations are value objects'''
    assert_equal(Duration(500), Duration(500))


def test_duration():
    '''Duration: A duration represents passed time'''
    start = datetime.datetime(2017, 10, 3, 17, 23, 41, 921081)
    end = datetime.datetime(2017, 10, 4, 19, 24, 41, 921081)
    seconds = (end - start).total_seconds()

    # Act
    duration = Duration(seconds).__repr__()

    # Assert
    assert_equal(duration, '<Duration: 1, 2:1:0 (d, h:m:s)>')
