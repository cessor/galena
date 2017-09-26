import datetime


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
        return (self._datetime - other._datetime).total_seconds()



