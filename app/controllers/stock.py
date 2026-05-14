from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.stock import StockAdjust, StockRead, StockSet
from app.services.stock import StockService


router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/products/{product_id}", response_model=StockRead)
def get_stock_for_product(product_id: int, db: Session = Depends(get_db)) -> StockRead:
    return StockService(db).get_stock_for_product(product_id)


@router.put("", response_model=StockRead)
def set_stock(payload: StockSet, db: Session = Depends(get_db)) -> StockRead:
    return StockService(db).set_stock(payload)


@router.post("/adjust", response_model=StockRead)
def adjust_stock(payload: StockAdjust, db: Session = Depends(get_db)) -> StockRead:
    return StockService(db).adjust_stock(payload)
