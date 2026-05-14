from sqlalchemy.orm import Session

from app.models import StockLevel
from app.repositories.products import ProductRepository
from app.repositories.stock import StockRepository
from app.schemas.stock import StockAdjust, StockSet
from app.services.exceptions import BadRequestError, NotFoundError


class StockService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.products = ProductRepository(db)
        self.stock = StockRepository(db)

    def get_stock_for_product(self, product_id: int) -> StockLevel:
        stock = self.stock.get_by_product_id(product_id)
        if stock is None:
            raise NotFoundError("Stock level not found")
        return stock

    def set_stock(self, payload: StockSet) -> StockLevel:
        if self.products.get(payload.product_id) is None:
            raise NotFoundError("Product not found")

        stock = self.stock.get_by_product_id(payload.product_id, for_update=True)
        if stock is None:
            stock = StockLevel(
                product_id=payload.product_id,
                quantity_on_hand=payload.quantity_on_hand,
                version=1,
            )
            self.stock.add(stock)
        else:
            stock.quantity_on_hand = payload.quantity_on_hand
            stock.version = (stock.version or 0) + 1

        self.db.commit()
        self.db.refresh(stock)
        return stock

    def adjust_stock(self, payload: StockAdjust) -> StockLevel:
        stock = self.stock.get_by_product_id(payload.product_id, for_update=True)
        if stock is None:
            raise NotFoundError("Stock level not found")

        new_quantity = stock.quantity_on_hand + payload.quantity_delta
        if new_quantity < 0:
            raise BadRequestError("Stock cannot go below zero")

        stock.quantity_on_hand = new_quantity
        stock.version = (stock.version or 0) + 1
        self.db.commit()
        self.db.refresh(stock)
        return stock
