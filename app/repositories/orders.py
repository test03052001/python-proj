from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import CustomerOrder, OrderLine
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[CustomerOrder]):
    model = CustomerOrder

    def get(self, entity_id: int) -> CustomerOrder | None:
        statement = (
            select(CustomerOrder)
            .options(
                selectinload(CustomerOrder.user),
                selectinload(CustomerOrder.lines).selectinload(OrderLine.product),
            )
            .where(CustomerOrder.id == entity_id)
        )
        return self.db.scalar(statement)

    def list_for_user(
        self,
        user_id: int | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[CustomerOrder]:
        statement = select(CustomerOrder).options(selectinload(CustomerOrder.user))
        if user_id is not None:
            statement = statement.where(CustomerOrder.user_id == user_id)
        statement = statement.order_by(CustomerOrder.created_at.desc()).offset(offset).limit(limit)
        return list(self.db.scalars(statement).all())
