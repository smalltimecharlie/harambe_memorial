from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal

router = APIRouter(prefix="/players", tags=["Players"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_players(db: Session = Depends(get_db)):
    from backend.models import User
    return db.query(User).all()
