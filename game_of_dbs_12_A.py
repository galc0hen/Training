from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
import datetime

engine = create_engine('sqlite:///midas.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
events_participants_association_table = Table('association', Base.metadata,
                                              Column('member_id', Integer, ForeignKey('members.id')),
                                              Column('event_id', Integer, ForeignKey('events.id')))


class MyQuery:
    def __init__(self, class_type):
        self.class_type = class_type
        self.session = Session()
        self.my_query_object = self.session.query(self.class_type).order_by(self.class_type.id)

    # Utility function.
    def format_class_name(self, number_of_instances_in_class):
        parsed_class_name = str(self.class_type).split('.')[-1].split('\'')[0]
        if number_of_instances_in_class == 1:
            return parsed_class_name
        # Return name in plural.
        return parsed_class_name + 's'  # I did not apply here all English plural grammar rules.

    def __repr__(self):
        number_of_instances_in_class = len(self.session.query(self.class_type).all())
        class_name_formatted = self.format_class_name(number_of_instances_in_class)
        return f'<{number_of_instances_in_class} {class_name_formatted}>'

    def refine(self, condition):
        # Condition can be a keyword or an sqlalchemy filter.
        print(condition)


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    last_name = Column(String(30))
    role = Column(String(256))
    city = Column(String(256))

    youth_group_id = Column(Integer, ForeignKey("youth_groups.id"))
    youth_group = relationship("YouthGroup", back_populates="members")
    events = relationship("Event", secondary=events_participants_association_table, back_populates="participants")

    @classmethod
    def get(cls):
        return MyQuery(cls)

    def __repr__(self):
        return self.name


class YouthGroup(Base):
    __tablename__ = 'youth_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    city = Column(String(256))

    members = relationship("Member", order_by=Member.id, back_populates="youth_group")

    def __repr__(self):
        return self.name


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    location = Column(String(256))
    date = Column(String(30))

    participants = relationship("Member", secondary=events_participants_association_table, back_populates="events")

    def __repr__(self):
        return self.name


def test_insertion_to_db(session, test_member, test_youth_group, test_event):
    assert test_member is session.query(Member).filter_by(name='John').first()
    assert test_youth_group is session.query(YouthGroup).filter_by(name='Tzofim').first()
    assert test_event is session.query(Event).filter_by(name='Purim Party').first()
    purim_party = session.query(Event).filter_by(name='Purim Party').first()
    assert purim_party.participants == test_event.participants
    print('Tests succeeded.')


def return_all_members_not_from_same_city_as_youth_group(session):
    result = []
    for member in session.query(Member).order_by(Member.id):
        if member.city != member.youth_group.city:
            result.append(member)
    return result


def return_last_event_date_for_each_member(session):
    result = {}
    for member in session.query(Member).order_by(Member.id):
        if not member.events:
            result[member.name] = 'No Events.'
            continue
        last_event = member.events[0]
        events = member.events[1:]
        for event in events:
            if event.date > last_event.date:
                last_event = event
        result[member.name] = last_event.date
    return result


def return_number_of_members_for_each_youth_group(session):
    result = {}
    for youth_group in session.query(YouthGroup).order_by(YouthGroup.id):
        result[youth_group.name] = len(youth_group.members)
    return result


def return_number_of_participating_youth_groups_in_each_event(session):
    result = {}
    for event in session.query(Event).order_by(Event.id):
        number_of_different_youth_groups = []
        for participant in event.participants:
            if participant.youth_group.name not in number_of_different_youth_groups:
                number_of_different_youth_groups.append(participant.youth_group.name)
        result[event.name] = len(number_of_different_youth_groups)
    return result


def return_number_of_people_you_may_know(session):
    result = {}
    for member in session.query(Member).order_by(Member.id):
        people_member_may_know = []
        for event in member.events:
            for participant in event.participants:
                if participant != member and participant.name not in event.participants:
                    people_member_may_know.append(participant.name)
        result[member.name] = people_member_may_know
    return result


def main():
    session = Session()
    Base.metadata.create_all(engine)
    # Initiate entities.
    tzofim = YouthGroup(name='Tzofim', city='Raanana')
    tzofei_yam = YouthGroup(name='Tzofei Yam', city='Natanya')
    john = Member(name='John', last_name='Smith', role='Team Leader', city='Kfar Saba')
    bill = Member(name='Bill', last_name='Jackson', role='Scout', city='Or Yehuda')
    mike = Member(name='Mike', last_name='Jones', role='Scout', city='Raanana')
    purim_party = Event(name='Purim Party', location='Tel Aviv', date=datetime.date(2018, 3, 15).isoformat())
    passover_party = Event(name='Passover Party', location='Jerusalem', date=datetime.date(2018, 4, 15).isoformat())
    # Add members to youth groups.
    tzofim.members.append(john)
    tzofim.members.append(mike)
    tzofei_yam.members.append(bill)
    # Add participants to events.
    purim_party.participants.append(john)
    purim_party.participants.append(bill)
    passover_party.participants.append(bill)
    # Add entities to table and commit.
    session.add_all([tzofim, tzofei_yam, john, bill, mike, purim_party, passover_party])
    session.commit()
    # Tests and queries.
    test_insertion_to_db(session, john, tzofim, purim_party)
    print(f'Members living in a different city than where their youth group is: '
          f'{return_all_members_not_from_same_city_as_youth_group(session)}')
    print(f'Last date a member participated in an event, for each member: '
          f'{return_last_event_date_for_each_member(session)}')
    print(f'Number of members in each youth group: '
          f'{return_number_of_members_for_each_youth_group(session)}')
    print(f'Number of participating youth groups in each event: '
          f'{return_number_of_participating_youth_groups_in_each_event(session)}')
    print(f'For each member, number of people you may know: '
          f'{return_number_of_people_you_may_know(session)}')
    print(type(Member.get()))


if __name__ == '__main__':
    main()
