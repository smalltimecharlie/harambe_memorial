from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    handicap = Column(Integer, nullable=True)
    role = Column(String, default="player")
    
    rounds = relationship("Round", back_populates="player")

# Course Model
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    par = Column(Integer, nullable=False)
    slope_rating = Column(Float, nullable=False)
    course_rating = Column(Float, nullable=False)
    
    rounds = relationship("Round", back_populates="course")

# Competition Model
class Competition(Base):
    __tablename__ = "competitions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    
    rounds = relationship("Round", back_populates="competition")

# Round Model
class Round(Base):
    __tablename__ = "rounds"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    score = Column(Integer, nullable=False)
    date_played = Column(DateTime, default=datetime.utcnow)
    
    player = relationship("User", back_populates="rounds")
    competition = relationship("Competition", back_populates="rounds")
    course = relationship("Course", back_populates="rounds")
    scores = relationship("Score", back_populates="round")

# Score Model
class Score(Base):
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)
    hole_number = Column(Integer, nullable=False)
    strokes = Column(Integer, nullable=False)
    
    round = relationship("Round", back_populates="scores")

