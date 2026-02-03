from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from .models import Role

# User Schemas
class UserBase(BaseModel):
    username: str
    role: Role
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Inventory Schemas
class InventoryBase(BaseModel):
    name: str
    kit_id: str
    model: Optional[str] = None
    serial_number: Optional[str] = None
    category: str
    quantity: int = 1
    status: str
    # New Hierarchical Fields
    state: Optional[str] = "Warehouse"
    district: Optional[str] = None
    institution: Optional[str] = None

    qr_code: Optional[str] = None
    description: Optional[str] = None
    batch_id: Optional[int] = None

    @field_validator('serial_number', 'qr_code', 'model', 'description', 'institution', 'district', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)

# Batch & Participant Schemas
class ParticipantBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    batch_id: int
    model_config = ConfigDict(from_attributes=True)

class BatchBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    location: str

class BatchCreate(BatchBase):
    training_id: int

class Batch(BatchBase):
    id: int
    training_id: int
    participants: List[Participant] = []
    model_config = ConfigDict(from_attributes=True)

# Training Schemas
class TrainingBase(BaseModel):
    title: str
    instructor: str
    date: str
    participants_count: int = 0
    status: str
    ndu_mapping_id: Optional[str] = None

class TrainingCreate(TrainingBase):
    pass

class Training(TrainingBase):
    id: int
    batches: List[Batch] = []

    model_config = ConfigDict(from_attributes=True)

# Content Schemas
class ContentBase(BaseModel):
    title: str
    category: str
    duration_minutes: int
    tags: str
    ndu_reference_id: Optional[str] = None
    # Mandatory RFP Flags
    has_safety_checklist: bool = False
    has_troubleshooting: bool = False
    has_assessment_cues: bool = False
    quality_checked: bool = False

class ContentCreate(ContentBase):
    pass

class ContentOut(ContentBase):
    id: int
    approval_status: str

    model_config = ConfigDict(from_attributes=True)
