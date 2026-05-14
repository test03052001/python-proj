from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    model = Product

    def get(self, entity_id: int) -> Product | None:
        statement = (
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == entity_id)
        )
        return self.db.scalar(statement)

    def get_by_sku(self, sku: str) -> Product | None:
        statement = select(Product).where(Product.sku == sku)
        return self.db.scalar(statement)

    def list(
        self,
        offset: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ) -> list[Product]:
        statement = select(Product).options(selectinload(Product.category))
        if active_only:
            statement = statement.where(Product.active.is_(True))
        statement = statement.offset(offset).limit(limit)
        return list(self.db.scalars(statement).all())
