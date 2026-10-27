import uuid
from collections.abc import Callable
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import get_user_by_id
from app.db.session import get_db
from app.models.enums import UserRole, UserStatus


bearer_scheme = HTTPBearer(
    auto_error=False,
)

def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
        db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Authorization header missing.",
                "code": "AUTH_HEADER_MISSING",
            },
        )
    
    payload = decode_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid or expired token.",
                "code": "AUTH_INVALID_TOKEN",
            },
        )

    subject = payload.get("sub")

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token subject missing.",
                "code": "AUTH_TOKEN_SUBJECT_MISSING",
            },
        )

    try:
        user_id = uuid.UUID(subject)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid token subject format.",
                "code": "AUTH_INVALID_TOKEN_SUBJECT",
            },
        )

    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "User not found.",
                "code": "AUTH_USER_NOT_FOUND",
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

    return user

def require_role(
        *allowed_roles: UserRole
        ) -> Callable:
    def role_dependency(
            current_user: User = Depends(
                get_current_user
                ),
                ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Insufficient permissions.",
                    "code": "AUTH_INSUFFICIENT_ROLE",
                },
            )
        
        return current_user
    
    return role_dependency