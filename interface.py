from collections import namedtuple


class Entry(namedtuple('Entry', ['ip', 'protocol', 'timestamp'])):
    pass
