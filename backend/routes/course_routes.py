from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal

router = APIRouter(prefix="/courses", tags=["Courses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    from backend.models import Course
    return db.query(Course).all()
