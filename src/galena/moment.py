import datetime


class Duration(object):
    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    UNITS = [DAY, HOUR, MINUTE, SECOND]

    def __init__(self, seconds):
        self._seconds = seconds

    def _unit_values(self):
        value = self._seconds
        for unit in self.UNITS:
            yield int(value // unit)
            value = value % unit

    def __repr__(self):
        return '<Duration: %s>' % str(self)

    def __str__(self):
        return '%s, %s:%s:%s (d, h:m:s)' % tuple(self._unit_values())

    def __eq__(self, other):
        return self._seconds == other._seconds


class Moment(object):
    PATTERN = '%Y-%m-%d_%H-%M'

    def __init__(self, datetime):
        self._datetime = datetime

    @classmethod
    def now(cls):
        return Moment(datetime.datetime.now())

    @classmethod
    def from_string(cls, string):
        date = datetime.datetime.strptime(string, Moment.PATTERN)
        return Moment(date)

    def __str__(self):
        return datetime.datetime.strftime(self._datetime, Moment.PATTERN)

    def __repr__(self):
        return '<Moment: %s>' % str(self)

    def __sub__(self, other):
        seconds = (self._datetime - other._datetime).total_seconds()
        return Duration(seconds)
