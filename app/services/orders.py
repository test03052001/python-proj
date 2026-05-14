from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import CustomerOrder, OrderLine
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.repositories.stock import StockRepository
from app.repositories.users import UserRepository
from app.schemas.orders import OrderCreate, OrderStatus, OrderStatusUpdate
from app.services.exceptions import BadRequestError, NotFoundError


class OrderService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.orders = OrderRepository(db)
        self.products = ProductRepository(db)
        self.stock = StockRepository(db)
        self.users = UserRepository(db)

    def list_orders(
        self,
        user_id: int | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[CustomerOrder]:
        return self.orders.list_for_user(user_id=user_id, offset=offset, limit=limit)

    def get_order(self, order_id: int) -> CustomerOrder:
        order = self.orders.get(order_id)
        if order is None:
            raise NotFoundError("Order not found")
        return order

    def create_order(self, payload: OrderCreate) -> CustomerOrder:
        user = self.users.get(payload.user_id)
        if user is None or not user.active:
            raise NotFoundError("Active user not found")

        order = CustomerOrder(
            user_id=payload.user_id,
            status=OrderStatus.pending.value,
            total_amount=Decimal("0.0000"),
        )
        total_amount = Decimal("0.0000")

        for item in payload.lines:
            product = self.products.get(item.product_id)
            if product is None or not product.active:
                raise NotFoundError(f"Active product {item.product_id} not found")

            stock = self.stock.get_by_product_id(item.product_id, for_update=True)
            if stock is None or stock.quantity_on_hand < item.quantity:
                raise BadRequestError(f"Not enough stock for product {item.product_id}")

            stock.quantity_on_hand -= item.quantity
            stock.version = (stock.version or 0) + 1
            line_total = product.unit_price * item.quantity
            total_amount += line_total
            order.lines.append(
                OrderLine(
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.unit_price,
                )
            )

        order.total_amount = total_amount
        self.orders.add(order)
        self.db.commit()
        return self.get_order(order.id)

    def update_status(self, order_id: int, payload: OrderStatusUpdate) -> CustomerOrder:
        order = self.get_order(order_id)
        if order.status == OrderStatus.cancelled.value:
            raise BadRequestError("Cancelled orders cannot be changed")
        order.status = payload.status.value
        self.db.commit()
        return self.get_order(order.id)
