from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal
from .auth import get_current_active_user, get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Inventory])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    items = crud.get_inventory(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schemas.Inventory)
def create_item(item: schemas.InventoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # In a real app, strict role check here (e.g. only Admin/SuperAdmin)
    try:
        return crud.create_inventory_item(db=db, item=item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/audit-export")
def audit_export_action(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    crud.log_audit(db, current_user.id, "EXPORT_REPORT", "User exported Inventory CSV Report")
    return {"message": "Logged"}

# Correlation Reporting (Clause 4.5 Hardening)
@router.get("/utilization")
def get_utilization_metrics(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    total = db.query(models.InventoryItem).count()
    if total == 0:
        return {"utilization_rate": 0, "allocated": 0, "total": 0}
        
    allocated = db.query(models.InventoryItem).filter(models.InventoryItem.batch_id != None).count()
    rate = round((allocated / total) * 100, 2)
    
    return {
        "utilization_rate": rate,
        "allocated_kits": allocated,
        "total_kits": total,
        "correlation_status": "High" if rate > 70 else "Low"
    }

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Only Super Admin can delete inventory usually, but let's allow Admin for now as per plan
    success = crud.delete_inventory_item(db, item_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None
