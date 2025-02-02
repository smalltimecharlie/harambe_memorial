from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./golf_society.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    handicap = Column(Float, default=0.0)

class Competition(Base):
    __tablename__ = "competitions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    date = Column(String)

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    competition_id = Column(Integer, ForeignKey("competitions.id"))
    total_score = Column(Integer)
    hole_by_hole_scores = Column(JSON)  # List of hole scores
    points = Column(Integer, default=0)  # For Stableford/Bogey scoring
    player = relationship("Player")
    competition = relationship("Competition")

# Handicap Calculation
def calculate_course_handicap(player_handicap: float, course_rating: float, slope_rating: float) -> float:
    return round((player_handicap * (slope_rating / 113)) + (course_rating - 72), 1)

# Super Par Calculation
def calculate_super_par(hole_scores: list, par_values: list, shots_received: list) -> int:
    points = 0
    for hole_score, par, shots in zip(hole_scores, par_values, shots_received):
        if hole_score == par:
            hole_points = 1
        elif hole_score == par - 1:
            hole_points = 2
        elif hole_score == par - 2:
            hole_points = 4
        else:
            hole_points = 0
        
        if shots > 0:
            hole_points *= 2
        
        points += hole_points
    return points

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI App
app = FastAPI()

@app.post("/players/")
def create_player(name: str, handicap: float = 0.0, db: Session = Depends(get_db)):
    player = Player(name=name, handicap=handicap)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

@app.get("/players/")
def get_players(db: Session = Depends(get_db)):
    return db.query(Player).all()

@app.post("/competitions/")
def create_competition(name: str, date: str, db: Session = Depends(get_db)):
    competition = Competition(name=name, date=date)
    db.add(competition)
    db.commit()
    db.refresh(competition)
    return competition

@app.post("/scores/")
def record_score(player_id: int, competition_id: int, hole_by_hole_scores: list, par_values: list, shots_received: list, db: Session = Depends(get_db)):
    total_score = sum(hole_by_hole_scores)
    points = calculate_super_par(hole_by_hole_scores, par_values, shots_received)
    new_score = Score(player_id=player_id, competition_id=competition_id, total_score=total_score, hole_by_hole_scores=hole_by_hole_scores, points=points)
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score

@app.get("/leaderboard/")
def get_leaderboard(competition_id: int, db: Session = Depends(get_db)):
    scores = db.query(Score).filter(Score.competition_id == competition_id).all()
    leaderboard = sorted(scores, key=lambda x: x.points, reverse=True)
    return [{"player": score.player.name, "points": score.points} for score in leaderboard]

@app.get("/calculate_handicap/")
def get_course_handicap(player_handicap: float, course_rating: float, slope_rating: float):
    return {"course_handicap": calculate_course_handicap(player_handicap, course_rating, slope_rating)}

# Create Tables
Base.metadata.create_all(bind=engine)
