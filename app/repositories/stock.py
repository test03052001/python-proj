from sqlalchemy import select

from app.models import StockLevel
from app.repositories.base import BaseRepository


class StockRepository(BaseRepository[StockLevel]):
    model = StockLevel

    def get_by_product_id(self, product_id: int, for_update: bool = False) -> StockLevel | None:
        statement = select(StockLevel).where(StockLevel.product_id == product_id)
        if for_update:
            statement = statement.with_for_update()
        return self.db.scalar(statement)
