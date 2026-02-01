from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Audit Helper
def log_audit(db: Session, user_id: int | None, action: str, details: str):
    audit = models.AuditLog(user_id=user_id, action=action, details=details)
    db.add(audit)
    db.commit()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, 
        hashed_password=hashed_password, 
        role=user.role,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # No current_user context here easily available during init, skipping audit for init usually
    return db_user

def get_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InventoryItem).offset(skip).limit(limit).all()

def create_inventory_item(db: Session, item: schemas.InventoryCreate, user_id: int):
    # Check if kit_id exists
    existing = db.query(models.InventoryItem).filter(models.InventoryItem.kit_id == item.kit_id).first()
    if existing:
        raise Exception(f"Kit ID {item.kit_id} already exists")

    db_item = models.InventoryItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Log Strict Transaction (RFP Clause 4.4)
    location_str = f"{item.state}/{item.district or '-'}/{item.institution or '-'}"
    transaction = models.InventoryTransaction(
        kit_id=item.kit_id,
        action_type="INITIAL_ALLOCATION",
        from_location="VENDOR",
        to_location=location_str,
        user_id=user_id
    )
    db.add(transaction)
    db.commit()

    log_audit(db, user_id, "CREATE_INVENTORY", f"Created Item {item.name} (Kit ID: {item.kit_id})")
    return db_item

def get_trainings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TrainingProgram).offset(skip).limit(limit).all()

def create_training(db: Session, training: schemas.TrainingCreate, user_id: int):
    db_training = models.TrainingProgram(**training.model_dump())
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    
    log_audit(db, user_id, "CREATE_TRAINING", f"Created Program {training.title}")
    return db_training

def delete_inventory_item(db: Session, item_id: int, user_id: int):
    item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if item:
        details = f"Deleted Item {item.name} (Kit ID: {item.kit_id})"
        db.delete(item)
        db.commit()
        log_audit(db, user_id, "DELETE_INVENTORY", details)
        return True
    return False

def delete_training(db: Session, training_id: int, user_id: int):
    training = db.query(models.TrainingProgram).filter(models.TrainingProgram.id == training_id).first()
    if training:
        details = f"Deleted Program {training.title}"
        db.delete(training)
        db.commit()
        log_audit(db, user_id, "DELETE_TRAINING", details)
        return True
    return False

def get_recent_audits(db: Session, limit: int = 5):
    return db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).limit(limit).all()
