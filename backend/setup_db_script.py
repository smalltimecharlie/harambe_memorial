from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.models import Base
from backend.models import User, Course, Competition, Round, Score
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./golf_society.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize database
def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    # Insert sample users
    session = SessionLocal()
    sample_users = [
        User(name="Tiger Woods", handicap=3, role="player"),
        User(name="Rory McIlroy", handicap=2, role="player"),
        User(name="Jon Rahm", handicap=1, role="player"),
        User(name="Admin User", handicap=0, role="admin")
    ]
    session.add_all(sample_users)
    session.commit()
    session.close()
    print("Sample users added to the database.")
    
    # Sample players
    players = [
        User(name="Tiger Woods", handicap=3),
        User(name="Rory McIlroy", handicap=2),
        User(name="Jon Rahm", handicap=1)
    ]
    session.add_all(players)
    session.commit()
    
    # Sample courses
    courses = [
        Course(name="Augusta National", location="Georgia, USA", par=72, slope_rating=113.0, course_rating=75.0),
        Course(name="St. Andrews", location="Scotland", par=72, slope_rating=110.0, course_rating=74.0)
    ]
    session.add_all(courses)
    session.commit()
    
    # Sample competitions
    competitions = [
        Competition(name="Masters Tournament", type="Stroke Play", start_date=datetime.utcnow()),
        Competition(name="The Open Championship", type="Stroke Play", start_date=datetime.utcnow())
    ]
    session.add_all(competitions)
    session.commit()
    
    # Sample rounds
    rounds = [
        Round(player_id=players[0].id, competition_id=competitions[0].id, course_id=courses[0].id, score=70, date_played=datetime.utcnow()),
        Round(player_id=players[1].id, competition_id=competitions[0].id, course_id=courses[0].id, score=68, date_played=datetime.utcnow()),
        Round(player_id=players[2].id, competition_id=competitions[0].id, course_id=courses[0].id, score=72, date_played=datetime.utcnow()),
        Round(player_id=players[0].id, competition_id=competitions[1].id, course_id=courses[1].id, score=71, date_played=datetime.utcnow()),
        Round(player_id=players[1].id, competition_id=competitions[1].id, course_id=courses[1].id, score=69, date_played=datetime.utcnow()),
        Round(player_id=players[2].id, competition_id=competitions[1].id, course_id=courses[1].id, score=73, date_played=datetime.utcnow())
    ]
    session.add_all(rounds)
    session.commit()
    
    # Sample scores (hole-by-hole for first round)
    scores = [
        Score(round_id=rounds[0].id, hole_number=i, strokes=4) for i in range(1, 19)
    ]
    session.add_all(scores)
    session.commit()
    
    session.close()
    print("Database initialized with sample data.")

# Function to drop tables
def drop_db():
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped.")

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
