from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, crud
from ..database import SessionLocal
from .auth import get_current_active_user, get_db
from ..services.ndu import MockNDUService

router = APIRouter()

@router.post("/sync/content/{content_id}")
def sync_content_to_ndu(content_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    content = db.query(models.ContentItem).filter(models.ContentItem.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    service = MockNDUService(db)
    success, message = service.sync_content(content)
    
    if not success:
        raise HTTPException(status_code=502, detail=message)
        
    return {"message": message, "ndu_id": content.ndu_reference_id}

@router.post("/sync/training/{training_id}")
def sync_training_to_ndu(training_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    training = db.query(models.TrainingProgram).filter(models.TrainingProgram.id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail="Training program not found")
    
    service = MockNDUService(db)
    success, message = service.sync_training(training) # Fixed method name from sync_content to sync_training in original plan thought, ensuring code is correct
    
    if not success:
        raise HTTPException(status_code=502, detail=message)
        
    return {"message": message, "ndu_id": training.ndu_mapping_id}
