from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRead
from app. schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import register_customer, authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register", 
    response_model=UserRead, 
    status_code=status.HTTP_201_CREATED
    )
def register(
        data: RegisterRequest, 
        db: Session = Depends(get_db)
    ):
    return register_customer(db, data)

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
        data: LoginRequest,
        db: Session = Depends(get_db)
    ):
    token = authenticate_user(db, data)
    return TokenResponse(access_token=token)

@router.get(
    "/me",
    response_model=UserRead,
)
def get_me(
        current_user: User = Depends(get_current_user)
    ):
    return current_user