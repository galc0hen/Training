import datetime as dt


def index(data):
    """
    Index the given entries.

    :note: May be called multiple times.

    :param data: A list of 'Entry' instances to index.
    """
    pass


def get_device_histogram(ip, n):
    """
    Return the latest 'n' entries for the given 'ip'.
    """
    return [
        {'timestamp': dt.datetime.now(), 'protocol': 'DNS'}
    ]


def get_devices_status():
    """
    Return a list of every ip and the latest time it was seen it.
    """
    return [
        ('4.2.2.4', dt.datetime.now()),
        ('8.8.8.8', dt.datetime.now())
    ]
