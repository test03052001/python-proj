from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.categories import CategoryRead


class ProductCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    unit_price: Decimal = Field(gt=0, max_digits=19, decimal_places=4)
    category_id: int


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    unit_price: Decimal | None = Field(default=None, gt=0, max_digits=19, decimal_places=4)
    category_id: int | None = None
    active: bool | None = None


class ProductRead(BaseModel):
    id: int
    sku: str
    name: str
    unit_price: Decimal
    category_id: int
    active: bool
    category: CategoryRead | None = None

    model_config = ConfigDict(from_attributes=True)
