from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal

router = APIRouter(prefix="/rounds", tags=["Rounds"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_rounds(db: Session = Depends(get_db)):
    from backend.models import Round  # Lazy import to avoid circular import issues
    return db.query(Round).all()
