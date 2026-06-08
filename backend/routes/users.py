from fastapi import APIRouter
from fastapi import Depends
from auth import verify_token
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db

from models import User

from schemas import UserCreate, UserLogin
from auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()
security = HTTPBearer()
@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }
@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "error": "User not found"
        }

    if not verify_password(
        user.password,
        db_user.password
    ):
        return {
            "error": "Invalid password"
        }

    token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/profile")
def profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        return {
            "error": "Invalid token"
        }

    return {
        "message": "Protected Route Accessed",
        "user": payload["sub"]
    }