from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
import os
import math

# Security setup
API_KEY = "mysecureapikey"
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./golf_society.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Pydantic Models
class PlayerCreate(BaseModel):
    name: str
    handicap: float

class CourseCreate(BaseModel):
    name: str
    par_values: list[int]
    stroke_indexes: list[int]
    hole_yardages: list[int]

class CompetitionCreate(BaseModel):
    name: str
    date: str
    course_id: int
    competition_type: str

class ScoreCreate(BaseModel):
    player_id: int
    competition_id: int
    hole_by_hole_scores: list[int]

# Database Models
class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    handicap = Column(Float, default=0.0)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    par_values = Column(JSON)
    stroke_indexes = Column(JSON)
    hole_yardages = Column(JSON)

class Competition(Base):
    __tablename__ = "competitions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    date = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))
    competition_type = Column(String)
    course = relationship("Course")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    competition_id = Column(Integer, ForeignKey("competitions.id"))
    hole_by_hole_scores = Column(JSON)
    total_score = Column(Integer)
    stableford_points = Column(Integer, default=0)
    super_par_points = Column(Integer, default=0)
    eagles = Column(Integer, default=0)
    birdies = Column(Integer, default=0)
    pars = Column(Integer, default=0)
    bogeys = Column(Integer, default=0)
    doubles_or_worse = Column(Integer, default=0)
    twos = Column(Integer, default=0)
    player = relationship("Player")
    competition = relationship("Competition")

app = FastAPI()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_points(hole_scores, par_values):
    stableford_points = 0
    super_par_points = 0
    eagles = birdies = pars = bogeys = doubles_or_worse = twos = 0
    
    for hole_score, par in zip(hole_scores, par_values):
        score_diff = hole_score - par
        if hole_score == 2:
            twos += 1
        if score_diff == -2:
            stableford_points += 4
            super_par_points += 4
            eagles += 1
        elif score_diff == -1:
            stableford_points += 3
            super_par_points += 2
            birdies += 1
        elif score_diff == 0:
            stableford_points += 2
            super_par_points += 1
            pars += 1
        elif score_diff == 1:
            stableford_points += 1
            bogeys += 1
        else:
            doubles_or_worse += 1
    
    return stableford_points, super_par_points, eagles, birdies, pars, bogeys, doubles_or_worse, twos

@app.post("/competitions/", dependencies=[Depends(validate_api_key)])
def create_competition(competition: CompetitionCreate, db: Session = Depends(get_db)):
    db_competition = Competition(name=competition.name, date=competition.date, course_id=competition.course_id, competition_type=competition.competition_type)
    db.add(db_competition)
    db.commit()
    db.refresh(db_competition)
    return db_competition

@app.post("/scores/", dependencies=[Depends(validate_api_key)])
def record_score(score: ScoreCreate, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.id == score.competition_id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    
    course = competition.course
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    total_score = sum(score.hole_by_hole_scores)
    stableford_points, super_par_points, eagles, birdies, pars, bogeys, doubles_or_worse, twos = calculate_points(score.hole_by_hole_scores, course.par_values)
    
    new_score = Score(
        player_id=score.player_id,
        competition_id=score.competition_id,
        hole_by_hole_scores=score.hole_by_hole_scores,
        total_score=total_score,
        stableford_points=stableford_points,
        super_par_points=super_par_points,
        eagles=eagles,
        birdies=birdies,
        pars=pars,
        bogeys=bogeys,
        doubles_or_worse=doubles_or_worse,
        twos=twos
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    
    return new_score

# Create Tables
Base.metadata.create_all(bind=engine)

