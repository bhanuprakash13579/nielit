from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, models
from .auth import get_db, get_current_active_user

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # 1. Inventory Counts
    total_kits = db.query(models.InventoryItem).count()
    
    # 2. Batch/Training Counts
    active_batches = db.query(models.Batch).count() # Simplified for demo, ideally filter by date
    
    # 3. Content Counts (Splitting by Category for RFP Counters)
    content_query = db.query(models.ContentItem)
    total_content = content_query.count()
    practical_content = content_query.filter(models.ContentItem.category == "Practical").count()
    pedagogy_content = content_query.filter(models.ContentItem.category == "Pedagogy").count()
    
    # 4. Sync Status
    pending_syncs = content_query.filter(models.ContentItem.ndu_reference_id == None).count()
    
    # 5. Recent Logs (RFP Requirement: Audit Visibility)
    logs = crud.get_recent_audits(db)
    formatted_logs = [
        {
            "action": log.action,
            "user": f"User {log.user_id}" if log.user_id else "System",
            "time": log.timestamp.strftime("%H:%M %d-%b")
        } for log in logs
    ]

    return {
        "inventory": total_kits,
        "batches": active_batches,
        "content_total": total_content,
        "content_practical": practical_content,
        "content_pedagogy": pedagogy_content,
        "pending_syncs": pending_syncs,
        "user_role": current_user.role,
        "recent_logs": formatted_logs
    }
