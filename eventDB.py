import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event = Column(String, nullable=False)
    date = Column(Date, nullable=False)


engine = create_engine('sqlite:///events.db', echo=True, connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
query = session.query(Event)


def add_event(event: str, date: Date) -> None:
    """Add new event to table"""
    event = Event(event=event, date=date)
    session.add(event)
    session.commit()


def delete_event(event_id: int) -> None:
    """Delete event from table"""
    query.filter(Event.id == event_id).delete()
    session.commit()


def get_all_events(*args) -> list:
    """Returns all rows or filtered by date rows from the table as a list of Event objects """
    if args:
        return query.filter(Event.date.between(args[0], args[1])).all()
    return query.all()


def get_today_events() -> list:
    """Returns rows with today date from the table as a list of Event objects"""
    return query.filter(Event.date == datetime.date.today()).all()


def get_event_by_id(event_id: int) -> list:
    """Returns event by ID if exist"""
    return query.filter(Event.id == event_id).first()