from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class Role(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # Stored as string, validated as Enum in Schema
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    kit_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    model = Column(String)
    description = Column(Text, nullable=True)
    serial_number = Column(String, unique=True, nullable=True)
    category = Column(String, index=True)
    status = Column(String, default="AVAILABLE") # AVAILABLE, ALLOCATED, DAMAGED, CONSUMED
    
    # Hierarchical Location
    state = Column(String, nullable=True)
    district = Column(String, nullable=True)
    institution = Column(String, nullable=True)
    
    quantity = Column(Integer, default=1)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())
    qr_code = Column(String, nullable=True, unique=True)

    # Correlation Logic (Clause 4.4)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=True)

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    kit_id = Column(String, index=True) # Link by Kit ID
    action_type = Column(String) # ALLOCATE, RETURN, CONSUME, TRANSFER
    from_location = Column(String, nullable=True)
    to_location = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    training_id = Column(Integer, ForeignKey("trainings.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    location = Column(String)
    
    training = relationship("TrainingProgram", back_populates="batches")
    participants = relationship("Participant", back_populates="batch")

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    
    batch = relationship("Batch", back_populates="participants")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"))
    batch_id = Column(Integer, ForeignKey("batches.id"))
    date = Column(DateTime)
    status = Column(String) # PRESENT, ABSENT
    
class TrainingProgram(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    instructor = Column(String)
    date = Column(String) 
    participants_count = Column(Integer, default=0)
    status = Column(String) 
    ndu_mapping_id = Column(String, nullable=True) 

    batches = relationship("Batch", back_populates="training")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    details = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for failed login attempts
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class IntegrationLog(Base):
    __tablename__ = "integration_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String)
    payload = Column(Text)
    response = Column(Text)
    status = Column(String)
    error = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String) 
    duration_minutes = Column(Integer)
    tags = Column(String) 
    approval_status = Column(String, default="Pending")
    ndu_reference_id = Column(String, nullable=True)
    
    # Mandatory RFP Flags
    has_safety_checklist = Column(Boolean, default=False)
    has_troubleshooting = Column(Boolean, default=False)
    has_assessment_cues = Column(Boolean, default=False)
    quality_checked = Column(Boolean, default=False)
