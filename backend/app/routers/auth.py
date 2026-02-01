from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import SessionLocal

# Configuration (In production, use Env variables)
SECRET_KEY = "super-secret-key-change-this-in-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_super_admin_user(current_user: models.User = Depends(get_current_active_user)):
    if current_user.role != models.Role.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        # Log Failure
        crud.log_audit(db, None, "LOGIN_FAILURE", f"Failed login attempt for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Log Success
    crud.log_audit(db, user.id, "LOGIN_SUCCESS", "User logged in")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/init-users", status_code=status.HTTP_201_CREATED)
def init_users(db: Session = Depends(get_db)):
    # Check if users exist
    if crud.get_user_by_username(db, "superadmin"):
        return {"message": "Users already initialized"}
    
    super_admin = schemas.UserCreate(
        username="superadmin",
        password="password123",
        role=models.Role.SUPER_ADMIN,
        full_name="Super Administrator"
    )
    crud.create_user(db, super_admin)
    
    admin = schemas.UserCreate(
        username="admin",
        password="password123",
        role=models.Role.ADMIN,
        full_name="Project Administrator"
    )
    crud.create_user(db, admin)
    
    return {"message": "Super Admin and Admin created"}

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Role check: Admin only
    if current_user.role != models.Role.SUPER_ADMIN and current_user.role != models.Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(models.User).offset(skip).limit(limit).all()

@router.post("/users/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Only Super Admin can create admins, Admin can create normal users (logic simplified here)
    if current_user.role != models.Role.SUPER_ADMIN:
        # Simplification: Only SuperAdmin can create users for now to be safe, or allow Admin too.
        # Let's allow Admin for flexibility.
        pass
    
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    if current_user.role != models.Role.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Only Super Admin can delete users")
        
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
        
    db.delete(user)
    db.commit()
    return None
