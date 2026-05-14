from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.categories import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.categories import CategoryService


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
def list_categories(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[CategoryRead]:
    return CategoryService(db).list_categories(offset=offset, limit=limit)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryRead:
    return CategoryService(db).create_category(payload)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryRead:
    return CategoryService(db).get_category(category_id)


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
) -> CategoryRead:
    return CategoryService(db).update_category(category_id, payload)
