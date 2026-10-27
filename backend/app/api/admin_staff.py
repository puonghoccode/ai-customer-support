from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import require_role
from app.db.session import get_db
from app.models.user import User
from app.models.enums import UserRole
from app.schemas.user import StaffCreate, UserRead
from app.services.auth_service import create_staff

router = APIRouter(
    prefix="/admin/staff",
    tags=["Admin - Staff"],
)

@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def create_staff_account(
        data: StaffCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    return create_staff(db, data)