from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.products import ProductRead
from app.schemas.users import UserRead


class OrderStatus(str, Enum):
    pending = "PENDING"
    paid = "PAID"
    shipped = "SHIPPED"
    cancelled = "CANCELLED"


class OrderLineCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    user_id: int
    lines: list[OrderLineCreate] = Field(min_length=1)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderLineRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    product: ProductRead | None = None

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime
    total_amount: Decimal
    user: UserRead | None = None
    lines: list[OrderLineRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
