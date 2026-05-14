from sqlalchemy.orm import Session

from app.models import Category
from app.repositories.categories import CategoryRepository
from app.schemas.categories import CategoryCreate, CategoryUpdate
from app.services.exceptions import ConflictError, NotFoundError


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.categories = CategoryRepository(db)

    def list_categories(self, offset: int = 0, limit: int = 100) -> list[Category]:
        return self.categories.list(offset=offset, limit=limit)

    def get_category(self, category_id: int) -> Category:
        category = self.categories.get(category_id)
        if category is None:
            raise NotFoundError("Category not found")
        return category

    def create_category(self, payload: CategoryCreate) -> Category:
        if self.categories.get_by_name(payload.name):
            raise ConflictError("A category with this name already exists")

        category = Category(name=payload.name)
        self.categories.add(category)
        self.db.commit()
        return category

    def update_category(self, category_id: int, payload: CategoryUpdate) -> Category:
        category = self.get_category(category_id)
        existing = self.categories.get_by_name(payload.name) if payload.name else None
        if existing is not None and existing.id != category_id:
            raise ConflictError("A category with this name already exists")

        changes = payload.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)
        return category
