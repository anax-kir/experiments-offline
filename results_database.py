from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///results.db")

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    name = Column(String(50), unique=True)
    age = Column(String(20))
    gender = Column(String(30))
    education = Column(String(70))
    degree_subject = Column(String(200))
    occupation = Column(String(200))
    childhood_city = Column(String(200))
    longest_time_city = Column(String(200))
    now_city = Column(String(200))
    native_languages = Column(Text)
    other_languages = Column(Text)
    email = Column(String(200))

    def __init__(self,
                 date=None,
                 name=None,
                 age=None,
                 gender=None,
                 education=None,
                 degree_subject=None,
                 occupation=None,
                 childhood_city=None,
                 longest_time_city=None,
                 now_city=None,
                 native_languages=None,
                 other_languages=None,
                 email=None):
        self.date = date
        self.name = name
        self.age = age
        self.gender = gender
        self.education = education
        self.degree_subject = degree_subject
        self.occupation = occupation
        self.childhood_city = childhood_city
        self.longest_time_city = longest_time_city
        self.now_city = now_city
        self.native_languages = native_languages
        self.other_languages = other_languages
        self.email = email

    def __repr__(self):
        return '<Participant {} ({}, from {})>'.format(self.name, self.age, self.now_city)


class TrainingResult(Base):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
    sentence = Column(Text)
    rating = Column(Integer)
    participant_id = Column(Integer, ForeignKey('participants.id'))

    def __init__(self,
                 sentence=None,
                 rating=None,
                 participant_id=None):
        self.sentence = sentence
        self.rating = rating
        self.participant_id = participant_id


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)