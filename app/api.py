from fastapi import APIRouter

from app.controllers import categories, health, orders, products, stock, users


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(categories.router)
api_router.include_router(products.router)
api_router.include_router(stock.router)
api_router.include_router(orders.router)
