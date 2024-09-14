from datetime import timedelta
from backend.database.database import get_db
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database.models import User
from backend.schemas.schemas import UserCreate, UserResponse, Token, PasswordResetRequest
from backend.utils.utils import create_access_token, hash_password, verify_password, create_password_reset_token, verify_password_reset_token
from backend.utils.email_utils import send_email
from backend.utils.token_utils import create_confirmation_token
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
from jose import jwt
from jose.exceptions import JWTError

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# Environment variables and constants
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expiration time in minutes

# OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")

# Dependency to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=List[UserResponse], tags=["User"])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post('/register/', response_model=UserResponse, tags=["User"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the email or username already exists
    db_user_by_email = db.query(User).filter(User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user_by_username = db.query(User).filter(User.username == user.username).first()
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Prepare user data and create a new user
    user_data = user.dict(exclude={"password"})
    db_user = User(**user_data, password=hashed_password, is_confirmed=False)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate email confirmation token
    token = create_confirmation_token(email=user.email)
    confirmation_link = f"http://127.0.0.1:8005/api/users/confirm-email/?token={token}"
    email_body = f"Please confirm your email by clicking the following link: {confirmation_link}"
    
    # Send confirmation email
    send_email(to_email=user.email, subject="Email Confirmation", body=email_body)
    
    return db_user

@router.get('/confirm-email/', tags=["User"])
def confirm_email(token: str, db: Session = Depends(get_db)):
    try:
        # Decode the token to get the email address
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    # Retrieve the user by email
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the user is already confirmed
    if db_user.is_confirmed:
        return JSONResponse(content={"message": "Email already confirmed"}, status_code=status.HTTP_200_OK)
    
    # Update the user to set is_confirmed to True
    db_user.is_confirmed = True
    db.commit()
    db.refresh(db_user)
    
    return JSONResponse(content={"message": "Email confirmed successfully"}, status_code=status.HTTP_200_OK)

@router.post('/token', response_model=Token, tags=["User"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not confirmed",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/me', response_model=UserResponse, tags=["User"])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post('/forgot-password/', tags=["User"])
def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a password reset token
    reset_token = create_password_reset_token(data={"email": request.email})

    # Create a reset link
    reset_link = f"http://127.0.0.1:8005/api/user/reset-password/?token={reset_token}"
    email_body = f"Please use the following link to reset your password: {reset_link}"

    # Send the reset link via email
    send_email(to_email=user.email, subject="Password Reset", body=email_body)

    return {"message": "Password reset link sent to email"}

@router.post('/reset-password/', tags=["User"])
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    # Verify the token
    payload = verify_password_reset_token(token)
    email = payload.get("email")
    
    # Retrieve the user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash the new password and update the user
    hashed_password = hash_password(new_password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)

    return {"message": "Password reset successfully"}