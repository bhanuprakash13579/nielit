from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal
from .auth import get_current_active_user, get_db

router = APIRouter()

@router.post("/", response_model=schemas.ContentOut)
def create_content(content: schemas.ContentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Role check: Admin/SuperAdmin only
    if current_user.role not in [models.Role.ADMIN, models.Role.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_content = models.ContentItem(**content.model_dump())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    
    crud.log_audit(db, current_user.id, "CREATE_CONTENT", f"Created Content: {content.title}")
    return db_content

@router.get("/", response_model=List[schemas.ContentOut])
def read_content(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return db.query(models.ContentItem).offset(skip).limit(limit).all()
