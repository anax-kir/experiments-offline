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
    work_subject = Column(String(200))
    birth_city = Column(String(100))
    now_city = Column(String(100))
    mother_tongue = Column(String(200))
    other_langs = Column(String(200))

    def __init__(self,
                 date=None,
                 name=None,
                 age=None,
                 gender=None,
                 education=None,
                 work_subject=None,
                 birth_city=None,
                 now_city=None,
                 mother_tongue=None,
                 other_langs=None):
        self.date = date
        self.name = name
        self.age = age
        self.gender = gender
        self.education = education
        self.work_subject = work_subject
        self.birth_city = birth_city
        self.now_city = now_city
        self.mother_tongue = mother_tongue
        self.other_langs = other_langs

    def __repr__(self):
        return '<Participant {} ({}, from {})>'.format(self.name, self.age, self.now_city)


class TrainingResult(Base):
    __tablename__ = "training"
    id = Column(Integer, primary_key=True)
    sentence = Column(Text)
    score = Column(Integer)
    participant_id = Column(Integer, ForeignKey('participants.id'))

    def __init__(self,
                 sentence=None,
                 score=None,
                 participant_id=None):
        self.sentence = sentence
        self.score= score
        self.participant_id = participant_id


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)