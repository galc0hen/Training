from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
import datetime

engine = create_engine('sqlite:///midas.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
GLOBAL_SESSION = Session()
events_participants_association_table = Table('association', Base.metadata,
                                              Column('member_id', Integer, ForeignKey('members.id')),
                                              Column('event_id', Integer, ForeignKey('events.id')))


class MyQuery:
    def __init__(self, class_type):
        self.class_type = class_type
        self.session = GLOBAL_SESSION
        self.my_query_object = self.session.query(self.class_type)

    # Utility function.
    def format_class_name(self, number_of_instances_in_class):
        parsed_class_name = str(self.class_type).split('.')[-1].split('\'')[0]
        if number_of_instances_in_class == 1:
            return parsed_class_name
        # Return name in plural.
        return parsed_class_name + 's'  # I did not apply here all English plural grammar rules.

    def __repr__(self):
        number_of_instances = self.my_query_object.count()
        class_name_formatted = self.format_class_name(number_of_instances)
        return f'<{number_of_instances} {class_name_formatted}>'

    def refine(self, *args, **kwargs):
        # Assuming input is valid and is either a keyword argument or an sqlalchemy filter argument.
        refined_query = MyQuery(self.class_type)
        if args:
            refined_query.my_query_object = self.my_query_object.filter(*args)
        elif kwargs:
            refined_query.my_query_object = self.my_query_object.filter_by(**kwargs)
        return refined_query

    def first(self):
        return self.my_query_object.first()

    def distinct(self, parameter_to_count_by):
        return self.my_query_object.group_by(parameter_to_count_by).count()

    def join(self, table_to_join_with):
        refined_query = MyQuery(self.class_type)
        refined_query.my_query_object = self.my_query_object.join(table_to_join_with)
        return refined_query

    def order_by(self, parameter_to_order_by):
        refined_query = MyQuery(self.class_type)
        refined_query.my_query_object = self.my_query_object.order_by(parameter_to_order_by)
        return refined_query

    def __getitem__(self, index):
        refined_query = MyQuery(self.class_type)
        if type(index) == slice:
            refined_query.my_query_object = self.my_query_object.slice(index.start, index.stop)
        return refined_query


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

    @classmethod
    def get(cls):
        return MyQuery(cls)

    def __repr__(self):
        return self.name


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    location = Column(String(256))
    date = Column(String(30))

    participants = relationship("Member", secondary=events_participants_association_table, back_populates="events")

    @classmethod
    def get(cls):
        return MyQuery(cls)

    def __repr__(self):
        return self.name


def test_insertion_to_db(session, test_member, test_youth_group, test_event):
    assert test_member is session.query(Member).filter_by(name='John').first()
    assert test_youth_group is session.query(YouthGroup).filter_by(name='Tzofim').first()
    assert test_event is session.query(Event).filter_by(name='Purim Party').first()
    purim_party = session.query(Event).filter_by(name='Purim Party').first()
    assert purim_party.participants == test_event.participants
    print('Tests succeeded.')


def get_all_members_not_from_same_city_as_youth_group(session):
    result = []
    for member in session.query(Member).order_by(Member.id):
        if member.city != member.youth_group.city:
            result.append(member)
    return result


def get_last_event_date_for_each_member(session):
    # Assuming member full name is unique.
    result = {}
    for member in session.query(Member).order_by(Member.id):
        member_full_name = f'{member.name} {member.last_name}'
        if not member.events:
            result[member_full_name] = 'No Events.'
            continue
        last_event = member.events[0]
        events = member.events[1:]
        for event in events:
            if event.date > last_event.date:
                last_event = event
        result[member_full_name] = last_event.date
    return result


def get_number_of_members_for_each_youth_group(session):
    # Assuming youth group name is unique.
    result = {}
    for youth_group in session.query(YouthGroup).order_by(YouthGroup.id):
        result[youth_group.name] = len(youth_group.members)
    return result


def get_number_of_participating_youth_groups_in_each_event(session):
    # Assuming event name is unique.
    result = {}
    for event in session.query(Event).order_by(Event.id):
        number_of_different_youth_groups = []
        for participant in event.participants:
            if participant.youth_group.name not in number_of_different_youth_groups:
                number_of_different_youth_groups.append(participant.youth_group.name)
        result[event.name] = len(number_of_different_youth_groups)
    return result


def get_people_you_may_know(session):
    # Assuming member full name is unique.
    result = {}
    for member in session.query(Member).order_by(Member.id):
        member_full_name = f'{member.name} {member.last_name}'
        people_member_may_know = []
        for event in member.events:
            for participant in event.participants:
                participant_full_name = f'{participant.name} {participant.last_name}'
                if participant != member and participant_full_name not in people_member_may_know:
                    people_member_may_know.append(participant_full_name)
        result[member_full_name] = people_member_may_know
    return result


def main():
    session = GLOBAL_SESSION
    Base.metadata.create_all(engine)

    # Initiate entities.
    tzofim = YouthGroup(name='Tzofim', city='Raanana')
    tzofei_yam = YouthGroup(name='Tzofei Yam', city='Natanya')
    john = Member(name='John', last_name='Smith', role='Team Leader', city='Kfar Saba')
    bill = Member(name='Bill', last_name='Jackson', role='Scout', city='Or Yehuda')
    bill_miller = Member(name='Bill', last_name='Miller', role='Scout', city='Or Yehuda')
    mike = Member(name='Mike', last_name='Jones', role='Scout', city='Raanana')
    purim_party = Event(name='Purim Party', location='Tel Aviv', date=datetime.date(2018, 3, 15).isoformat())
    passover_party = Event(name='Passover Party', location='Jerusalem', date=datetime.date(2018, 4, 15).isoformat())

    # Add members to youthgroups.
    tzofim.members.append(john)
    tzofim.members.append(mike)
    tzofei_yam.members.append(bill)
    tzofei_yam.members.append(bill_miller)

    # Add participants to events.
    purim_party.participants.append(john)
    purim_party.participants.append(bill)
    passover_party.participants.append(bill)

    # Add entities to table and commit.
    session.add_all([tzofim, tzofei_yam, john, bill, bill_miller, mike, purim_party, passover_party])
    session.commit()

    # Tests and queries.
    # Expected output: 'Tests succeeded'.
    test_insertion_to_db(session, john, tzofim, purim_party)

    # Expected output: '[John, Bill, Bill]'.
    print(f'Members living in a different city than where their youth group is: '
          f'{get_all_members_not_from_same_city_as_youth_group(session)}')

    # Expected output:
    # '{'John Smith': '2018-03-15', 'Bill Jackson': '2018-04-15', \
    # 'Bill Miller': 'No Events.', 'Mike Jones': 'No Events.'}'.
    print(f'Last date a member participated in an event, for each member: '
          f'{get_last_event_date_for_each_member(session)}')

    # Expected output: {'Tzofim': 2, 'Tzofei Yam': 2}.
    print(f'Number of members in each youth group: '
          f'{get_number_of_members_for_each_youth_group(session)}')

    # Expected output: {'Purim Party': 2, 'Passover Party': 1}.
    print(f'Number of participating youth groups in each event: '
          f'{get_number_of_participating_youth_groups_in_each_event(session)}')

    # Expected output:
    # {'John Smith': ['Bill Jackson'], 'Bill Jackson': ['John Smith'], 'Bill Miller': [], 'Mike Jones': []}.
    print(f'For each member, list of people he may know: '
          f'{get_people_you_may_know(session)}')

    # Expected output: <1 YouthGroup>
    print(YouthGroup.get().refine(YouthGroup.city == 'Raanana'))

    # Expected output: <2 Members>
    print(Member.get().refine(role='Scout').refine(name='Bill'))

    # Expected output: 'John'.
    print(Member.get().order_by(Member.id).first())

    # Expected output: 3.
    print(Member.get().distinct(Member.name))

    # Expected output: <3 Members>
    print(Member.get().join(Member.events))

    # Expected output: Bill Mike Bill John
    ordered_by_role = Member.get().order_by(Member.last_name)
    ordered_by_role_str = ''
    for person_name in ordered_by_role.my_query_object:
        ordered_by_role_str += f'{person_name} '
    print(ordered_by_role_str)

    # Expected output: <1 Member>
    print(Member.get()[1:2])
    GLOBAL_SESSION.close()


if __name__ == '__main__':
    main()
