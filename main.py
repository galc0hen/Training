from implement_me import *
from datasets import *

BUFFER_SIZE = 100


def main():
    data_generator = s1wide()
    entry_list = []
    # I chose to implement some of the indexing logic here because in module implement_me.py,
    # the func "index" is said to get as a parameter a list of 'Entry' instances to index.
    for entry in data_generator:
        entry_list.append(entry)
        if len(entry_list) >= BUFFER_SIZE:
            index(entry_list)
            entry_list = []
    # Index last batch.
    index(entry_list)

    # Expected output: 16384 (128 unique IPs * 128 entries per IP).
    print(f'Number of DB entries: {GLOBAL_SESSION.query(Ip).count()}')
    # Expected output: list of 2 dicts, each containing a timestamp and a protocol for the given IP.
    # Constant IP 113.79.183.223 can be used for testing because Random was given a seed of 0 (in datasets.py).
    print(get_device_histogram('113.79.183.223', 2))
    # Expected output: list of 128 tuples, each containing an IP and a timestamp.
    print(get_devices_status())
    GLOBAL_SESSION.close()


if __name__ == '__main__':
    main()
