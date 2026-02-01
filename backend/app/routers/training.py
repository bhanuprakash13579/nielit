from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal
from .auth import get_current_active_user, get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Training])
def read_trainings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    trainings = crud.get_trainings(db, skip=skip, limit=limit)
    return trainings

@router.post("/", response_model=schemas.Training)
def create_training(training: schemas.TrainingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Role check
    if current_user.role != models.Role.ADMIN and current_user.role != models.Role.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.create_training(db=db, training=training, user_id=current_user.id)

@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training(training_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    if current_user.role != models.Role.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    success = crud.delete_training(db, training_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Training not found")
    return None
