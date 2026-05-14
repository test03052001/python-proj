from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.users import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[UserRead]:
    return UserService(db).list_users(offset=offset, limit=limit)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    return UserService(db).create_user(payload)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    return UserService(db).get_user(user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> UserRead:
    return UserService(db).update_user(user_id, payload)


@router.delete("/{user_id}", response_model=UserRead)
def deactivate_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    return UserService(db).deactivate_user(user_id)
