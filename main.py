from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os
import math

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
    grand_prix_points = Column(Float, default=0.0)  # Tracking Grand Prix points
    twos_count = Column(Integer, default=0)  # Tracking number of 2s
    eagles = Column(Integer, default=0)  # Tracking number of eagles
    birdies = Column(Integer, default=0)  # Tracking number of birdies
    pars = Column(Integer, default=0)  # Tracking number of pars
    bogeys = Column(Integer, default=0)  # Tracking number of bogeys
    doubles_or_worse = Column(Integer, default=0)  # Tracking double bogey or worse

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
    twos = Column(Integer, default=0)  # Number of twos in a round
    player = relationship("Player")
    competition = relationship("Competition")

# Grand Prix Scoring System
GRAND_PRIX_POINTS = [10, 8, 6, 5, 4, 3, 2, 1, 0]  # 9th place and beyond get 0 points

def update_grand_prix_leaderboard(db: Session):
    all_scores = db.query(Score).all()
    player_points = {}
    
    for score in all_scores:
        if score.player_id not in player_points:
            player_points[score.player_id] = 0
        player_points[score.player_id] += score.points
    
    sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
    
    i = 0
    while i < len(sorted_players):
        tied_players = [sorted_players[i]]
        while i + 1 < len(sorted_players) and sorted_players[i][1] == sorted_players[i + 1][1]:
            tied_players.append(sorted_players[i + 1])
            i += 1
        
        total_points = sum(GRAND_PRIX_POINTS[min(i, len(GRAND_PRIX_POINTS) - 1)] for _ in tied_players)
        shared_points = math.floor(total_points / len(tied_players) * 2) / 2  # Round down to nearest 0.5
        
        for player_id, _ in tied_players:
            player = db.query(Player).filter(Player.id == player_id).first()
            if player:
                player.grand_prix_points += shared_points
                db.commit()
        
        i += 1

@app.get("/overall_leaderboard/")
def get_overall_leaderboard(db: Session = Depends(get_db)):
    players = db.query(Player).order_by(Player.grand_prix_points.desc()).all()
    return [{"player": player.name, "grand_prix_points": player.grand_prix_points} for player in players]

@app.get("/twos_leaderboard/")
def get_twos_leaderboard(db: Session = Depends(get_db)):
    players = db.query(Player).order_by(Player.twos_count.desc()).all()
    return [{"player": player.name, "twos": player.twos_count} for player in players]

# Dummy Data Script
def populate_dummy_data():
    db = SessionLocal()
    db.add_all([
        Player(name="Alice", handicap=5.2),
        Player(name="Bob", handicap=10.4),
        Player(name="Charlie", handicap=15.6)
    ])
    db.commit()
    
    db.add_all([
        Competition(name="Spring Open", date="2025-04-10"),
        Competition(name="Summer Classic", date="2025-06-20")
    ])
    db.commit()
    
    db.add_all([
        Score(player_id=1, competition_id=1, total_score=75, hole_by_hole_scores=[4,4,3,5,4,4,3,5,4,4,4,3,4,4,4,5,3,4], points=30, twos=1),
        Score(player_id=2, competition_id=1, total_score=80, hole_by_hole_scores=[5,4,4,6,4,5,3,6,4,5,4,4,5,5,4,6,4,5], points=25, twos=0)
    ])
    db.commit()
    db.close()

if __name__ == "__main__":
    populate_dummy_data()

# Create Tables
Base.metadata.create_all(bind=engine)

