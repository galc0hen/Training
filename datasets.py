from random import Random
import ipaddr
import datetime as dt

from interface import Entry

LOWEST_IP = 2 ** 30  # 64.0.0.0
HIGHEST_IP = 2 ** 31  # 128.0.0.0
LOWEST_TIME = dt.datetime(2001, 1, 1).toordinal()
HIGHEST_TIME = dt.datetime(2016, 1, 1).toordinal()
PROTOCOLS = ['TCP', 'UDP', 'DNS', 'HTTP', 'SSH', 'FTP']

rnd = Random(0)


def _generate_dataset(number_of_ips, number_of_entries_per_ip):
    for ip_num in (rnd.randint(LOWEST_IP, HIGHEST_IP) for _ in range(number_of_ips)):
        for _ in range(number_of_entries_per_ip):
            yield Entry(str(ipaddr.IPAddress(ip_num)), protocol=rnd.choice(PROTOCOLS),
                        timestamp=dt.datetime.fromordinal(rnd.randint(LOWEST_TIME, HIGHEST_TIME)))


def s1wide():
    """
    Return a small data set, with a wide variety of ips.
    """
    number_of_ips = 128
    number_of_entries_per_ip = 128

    for entry in _generate_dataset(number_of_ips, number_of_entries_per_ip):
        yield entry


def s1narrow():
    """
    Return a small data set, with a small variey of ips.
    """
    number_of_ips = 16
    number_of_entries_per_ip = 1024

    for entry in _generate_dataset(number_of_ips, number_of_entries_per_ip):
        yield entry


def l1wide():
    """
    Return a large data set, with a wide variety of ips.
    """
    number_of_ips = 16384
    number_of_entries_per_ip = 128

    for entry in _generate_dataset(number_of_ips, number_of_entries_per_ip):
        yield entry


def l1narrow():
    """
    Return a large data set, with a small variety of ips.
    """
    number_of_ips = 128
    number_of_entries_per_ip = 16384

    for entry in _generate_dataset(number_of_ips, number_of_entries_per_ip):
        yield entry
