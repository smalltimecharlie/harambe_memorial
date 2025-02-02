from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal

router = APIRouter(prefix="/competitions", tags=["Competitions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_competitions(db: Session = Depends(get_db)):
    from backend.models import Competition  # Lazy import to avoid circular import issues
    return db.query(Competition).all()
