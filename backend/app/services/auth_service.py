from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import(
    create_access_token,
    hash_password,
    verify_password
)
from app.models.user import User
from app.models.enums import UserRole, UserStatus
from app.repositories.user_repository import(
    create_user,
    get_user_by_email,
)
from app.schemas.auth import(
    LoginRequest,
    RegisterRequest,
)
from app.schemas.user import StaffCreate

def register_customer(
        db: Session, 
        data: RegisterRequest
    ) -> User:
        email = data.email.lower()
        existing_user = get_user_by_email(db, email)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                      "message": "User with this email already exists.",
                      "code": "USER_EMAIL_ALREADY_EXISTS",
                }
            )
        user = User(
            email=email,
            password_hash=hash_password(data.password),
            full_name=data.full_name.strip(),
            phone=data.phone,
            company=data.company,
            role=UserRole.CUSTOMER,
            status=UserStatus.ACTIVE
        )

        return create_user(db, user)

def authenticate_user(
        db: Session,
        data: LoginRequest,
    ) -> str:
        user =  get_user_by_email(db, data.email.lower())
        if user is None or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Invalid email or password.",
                    "code": "AUTH_INVALID_CREDENTIALS",
                },
            )
        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "User account is inactive.",
                    "code": "AUTH_INACTIVE_ACCOUNT",
                },
            )

        user.last_login_at = datetime.now(timezone.utc)

        db.commit()

        return create_access_token(user.id, user.role)

def create_staff(
        db: Session,
        data: StaffCreate,
    ) -> User:
        email = data.email.lower()

        if get_user_by_email(db, email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "User with this email already exists.",
                    "code": "USER_EMAIL_ALREADY_EXISTS",
                },
            )

        staff = User(
            email=email,
            password_hash=hash_password(data.password),
            full_name=data.full_name.strip(),
            phone=data.phone,
            company=data.company,
            role=data.role,
            status=UserStatus.ACTIVE
        )

        return create_user(db, staff)