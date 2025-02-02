from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal

router = APIRouter(prefix="/scores", tags=["Scores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{round_id}")
def get_scores(round_id: int, db: Session = Depends(get_db)):
    from backend.models import Score
    return db.query(Score).filter(Score.round_id == round_id).all()
