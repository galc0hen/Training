from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from operator import itemgetter

engine = create_engine('sqlite:///ip_addresses.db', echo=False)
Base = declarative_base()


class Ip(Base):
    __tablename__ = 'ip_addresses'

    id = Column(Integer, primary_key=True)
    ip = Column(String(30))
    protocol = Column(String(30))
    timestamp = Column(DATETIME)

    def __repr__(self):
        return f'{self.ip}, {self.protocol}, {self.timestamp}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
GLOBAL_SESSION = Session()


def index(data):
    """
    Index the given entries.

    :note: May be called multiple times.

    :param data: A list of 'Entry' instances to index.
    """
    session = GLOBAL_SESSION
    for ip_address in data:
        session.add(Ip(ip=ip_address.ip, protocol=ip_address.protocol, timestamp=ip_address.timestamp))
    session.commit()


def get_device_histogram(ip, n):
    """
    Return the latest 'n' entries for the given 'ip'.
    """
    session = GLOBAL_SESSION
    result = []
    for entry in session.query(Ip).filter_by(ip=ip):
        result.append({'timestamp': entry.timestamp.isoformat(), 'protocol': entry.protocol})
    result.sort(key=itemgetter('timestamp'), reverse=True)
    return result[:n]


def get_devices_status():
    """
    Return a list of every ip and the latest time it was seen it.
    """
    session = GLOBAL_SESSION
    result_dict = {}
    for entry in session.query(Ip):
        if entry.ip not in result_dict:
            result_dict[entry.ip] = entry.timestamp.isoformat()
            continue
        if result_dict[entry.ip] < entry.timestamp.isoformat():
            result_dict[entry.ip] = entry.timestamp.isoformat()
    return list(result_dict.items())
