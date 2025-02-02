from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
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

# Grand Prix Scoring System
GRAND_PRIX_POINTS = [10, 8, 6, 5, 4, 3, 2, 1, 0]

# FastAPI App
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/players/", dependencies=[Depends(validate_api_key)])
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_player = Player(name=player.name, handicap=player.handicap)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@app.post("/courses/", dependencies=[Depends(validate_api_key)])
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(name=course.name, par_values=course.par_values, stroke_indexes=course.stroke_indexes, hole_yardages=course.hole_yardages)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

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
    
    player = db.query(Player).filter(Player.id == score.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    total_score = sum(score.hole_by_hole_scores)
    stableford_points, super_par_points, eagles, birdies, pars, bogeys, doubles_or_worse, twos = calculate_points(score.hole_by_hole_scores, course.par_values, course.stroke_indexes, player.handicap)
    
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

