from pydantic import BaseModel, ConfigDict, Field


class StockSet(BaseModel):
    product_id: int
    quantity_on_hand: int = Field(ge=0)


class StockAdjust(BaseModel):
    product_id: int
    quantity_delta: int


class StockRead(BaseModel):
    id: int
    product_id: int
    quantity_on_hand: int
    version: int | None = None

    model_config = ConfigDict(from_attributes=True)
